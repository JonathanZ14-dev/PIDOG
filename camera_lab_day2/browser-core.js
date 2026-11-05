/* Mirror of the teaching color rule, tested separately; not robot control. */
function rgbHSV(r,g,b){r/=255;g/=255;b/=255;const max=Math.max(r,g,b),min=Math.min(r,g,b),d=max-min;let h=0;if(d){if(max===r)h=((g-b)/d)%6;else if(max===g)h=(b-r)/d+2;else h=(r-g)/d+4;h/=6;if(h<0)h+=1}return [h,max===0?0:d/max,max]}
function bluePixel(rgb){const [h,s,v]=rgbHSV(...rgb);return h>=.52&&h<=.72&&s>=.40&&v>=.20}
function markerStatus(ratio,meanValue,threshold){return meanValue<.12?'unknown':ratio>=threshold?'marker_present':'marker_absent'}
if(typeof module!=='undefined')module.exports={rgbHSV,bluePixel,markerStatus};
