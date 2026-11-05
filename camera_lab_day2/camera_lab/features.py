"""Optional preprocessing lab: grayscale and Sobel edges from saved RGB JSON."""
import argparse
from pathlib import Path
from .core import Frame
from .files import load_frame, save_svg


def grayscale(frame):
    """Return a display-oriented weighted RGB grayscale Frame, not physical luminance."""
    values = [round(.299*r+.587*g+.114*b) for r,g,b in frame.pixels]
    return Frame(frame.width,frame.height,[[v,v,v] for v in values])


def sobel(frame):
    """Return an edge-strength display; leave one-pixel border black. No object labels."""
    gray = grayscale(frame)
    result = [[0,0,0] for _ in gray.pixels]
    kx = ((-1,0,1),(-2,0,2),(-1,0,1))
    ky = ((-1,-2,-1),(0,0,0),(1,2,1))
    for y in range(1,gray.height-1):
        for x in range(1,gray.width-1):
            gx=gy=0
            for j in range(3):
                for i in range(3):
                    value=gray.pixels[(y+j-1)*gray.width+x+i-1][0]
                    gx+=value*kx[j][i];gy+=value*ky[j][i]
            strength=min(255,round((abs(gx)+abs(gy))/8))
            result[y*gray.width+x]=[strength]*3
    return Frame(gray.width,gray.height,result)


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('image');p.add_argument('--out',required=True)
    args=p.parse_args();frame,_=load_frame(args.image)
    folder=Path(args.out);folder.mkdir(parents=True,exist_ok=False)
    save_svg(grayscale(frame),folder/'gray.svg')
    save_svg(sobel(frame),folder/'edges.svg')
    print('Saved gray.svg and edges.svg. Edges are intensity changes, not semantic boundaries.')


if __name__=='__main__':main()
