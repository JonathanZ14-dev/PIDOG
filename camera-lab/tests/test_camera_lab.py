import unittest
from unittest.mock import Mock, patch
from tempfile import TemporaryDirectory
from pathlib import Path
import json
from camera_lab.core import Frame, Settings, rgb_to_hsv, is_blue, blue_mask, analyze, suggest
from camera_lab.files import save_frame, load_frame, save_svg
from camera_lab.capture import CameraSource
from camera_lab.learn import fit_threshold, evaluate, load_rows


def solid(rgb):
    return Frame(6,4,[list(rgb) for _ in range(24)])


class PerceptionTests(unittest.TestCase):
    def test_bad_dimensions_and_pixels(self):
        for args in [(0,2,[]),(3,2,[[0,0,0]]),(3,2,[[256,0,0]]*6)]:
            with self.assertRaises(ValueError):Frame(*args)

    def test_row_major_coordinates(self):
        f=Frame(3,2,[[i,0,0] for i in range(6)])
        self.assertEqual(f.pixel(2,1),(5,0,0))
        with self.assertRaises(ValueError):f.pixel(-1,0)

    def test_hsv_units_and_colors(self):
        self.assertEqual(rgb_to_hsv((0,0,255)),(2/3,1,1))
        self.assertTrue(is_blue((0,0,255),Settings()))
        self.assertFalse(is_blue((255,0,0),Settings()))
        self.assertFalse(is_blue((10,10,10),Settings()))

    def test_invalid_settings(self):
        for kwargs in ({'area_threshold':0},{'hue_low':.9,'hue_high':.2},{'min_value':float('nan')}):
            with self.assertRaises(ValueError):Settings(**kwargs)

    def test_mask_and_full_blue(self):
        f=solid((0,0,255));r=analyze(f,Settings())
        self.assertEqual(sum(blue_mask(f,Settings())),24)
        self.assertEqual(r['full']['bbox'],[0,0,6,4])
        self.assertEqual(r['full']['centroid'],[2.5,1.5])
        self.assertEqual(r['zones']['center']['status'],'marker_present')

    def test_dark_is_unknown(self):
        r=analyze(solid((0,0,0)),Settings())
        self.assertEqual(r['zones']['center']['status'],'unknown')
        self.assertEqual(suggest(r),'STOP_AND_RECHECK_IMAGE')

    def test_red_is_not_free_space(self):
        r=analyze(solid((255,0,0)),Settings())
        self.assertEqual(r['zones']['center']['status'],'marker_absent')
        self.assertIn('NO_CLEARANCE',suggest(r))

    def test_boundary_threshold_inclusive(self):
        f=solid((255,255,255));f.pixels[2+2*6]=[0,0,255]
        r=analyze(f,Settings(area_threshold=.25))
        self.assertEqual(r['zones']['center']['blue_ratio'],.25)
        self.assertEqual(r['zones']['center']['status'],'marker_present')

    def test_unequal_width_partition_covers_bottom(self):
        f=Frame(7,5,[[255,255,255]]*35);r=analyze(f,Settings())
        self.assertEqual(sum(z['area'] for z in r['zones'].values()),7*3)

    def test_no_mask_has_no_bbox(self):
        r=analyze(solid((255,255,255)),Settings())
        self.assertIsNone(r['full']['bbox']);self.assertIsNone(r['full']['centroid'])

    def test_file_roundtrip_and_no_overwrite(self):
        with TemporaryDirectory() as d:
            p=Path(d)/'f.json';f=solid((1,2,3));save_frame(f,p,{'source':'test'})
            got,metadata=load_frame(p);self.assertEqual(got.pixels,f.pixels)
            self.assertEqual(metadata['source'],'test')
            with self.assertRaises(FileExistsError):save_frame(f,p)
            save_svg(f,Path(d)/'v.svg')
            import xml.etree.ElementTree as ET
            ET.parse(Path(d)/'v.svg')


class OwnershipTests(unittest.TestCase):
    @patch('camera_lab.capture.time.sleep')
    def test_capture_closes_after_success(self,sleep):
        camera=Mock();im=Mock(width=3,height=2);im.getdata.return_value=[(0,0,255)]*6
        camera.capture_image.return_value.convert.return_value.resize.return_value=im
        f,_=CameraSource(factory=lambda:camera).capture()
        self.assertEqual(f.width,3);camera.close.assert_called_once()
        camera.capture_image.return_value.convert.assert_called_once_with('RGB')

    def test_capture_closes_after_configuration_failure(self):
        camera=Mock();camera.configure.side_effect=RuntimeError('bad config')
        with self.assertRaises(RuntimeError):CameraSource(factory=lambda:camera).capture()
        camera.close.assert_called_once()

    @patch('camera_lab.capture.time.sleep')
    def test_capture_closes_after_read_failure(self,sleep):
        camera=Mock();camera.capture_image.side_effect=RuntimeError('bad capture')
        with self.assertRaises(RuntimeError):CameraSource(factory=lambda:camera).capture()
        camera.close.assert_called_once()


class LearningTests(unittest.TestCase):
    def test_fit_only_training_and_confusion(self):
        rows=[{'blue_ratio':0,'obstacle':0},{'blue_ratio':.2,'obstacle':1}]
        t=fit_threshold(rows);self.assertAlmostEqual(t,.1)
        self.assertEqual(evaluate(rows,t)['accuracy'],1)
        self.assertEqual(evaluate([{'blue_ratio':0,'obstacle':1}],t)['FN'],1)

    def test_scene_leakage_rejected(self):
        with TemporaryDirectory() as d:
            p=Path(d)/'x.csv';p.write_text('scene_id,split,blue_ratio,obstacle\na,train,0,0\na,test,.2,1\nb,validation,0,0\n')
            with self.assertRaises(ValueError):load_rows(p)

    def test_empty_training_rejected(self):
        with self.assertRaises(ValueError):fit_threshold([])


class FeatureTests(unittest.TestCase):
    def test_constant_has_no_edges(self):
        from camera_lab.features import sobel
        self.assertTrue(all(p == [0,0,0] for p in sobel(solid((100,100,100))).pixels))

    def test_boundary_has_edges_without_mutation(self):
        from camera_lab.features import sobel
        f=solid((0,0,0))
        for y in range(4):
            for x in range(3,6):f.pixels[y*6+x]=[255,255,255]
        before=[p[:] for p in f.pixels]
        self.assertTrue(any(p[0]>0 for p in sobel(f).pixels))
        self.assertEqual(f.pixels,before)


if __name__=='__main__':unittest.main()
