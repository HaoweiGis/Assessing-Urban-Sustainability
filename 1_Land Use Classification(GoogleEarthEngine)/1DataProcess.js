/*
 * @Author: Muhaowei
 * @Date: 2019-11-28 17:17:03
 * @LastEditors: Muhaowei
 * @LastEditTime: 2019-11-28 17:37:50
 * @Description: 
 */
var Sentinel2 = ee.ImageCollection("COPERNICUS/S2_SR"),
    GuangzhouP = ee.FeatureCollection("users/blackmhw/Guangzhou/GuangzhouP");

Map.addLayer(GuangzhouP)
var visParamsRGB = {
    bands: ['B4', 'B3', 'B2'],
    min: 925.7,
    max: 2235.3,
    gamma: 1,
};
var GuanzhouImgs = Sentinel2.filterDate('2019-01-15', '2019-08-15')
    .filterBounds(GuangzhouP).filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 10))
print(GuanzhouImgs)
var s2 = ee.ImageCollection("COPERNICUS/S2").filterDate('2019-05-01', '2020-01-01').filterBounds(GuangzhouP);
print(s2)

var cloudyImage = ee.Image('COPERNICUS/S2_SR/20190808T025549_20190808T030622_T49QGF').clip(GuangzhouP)
print(cloudyImage)
Map.addLayer(cloudyImage, visParamsRGB, 'GuanzhouImg')

// Bits 10 and 11 are clouds and cirrus, respectively.
var cloudBitMask = ee.Number(2).pow(10).int();
var cirrusBitMask = ee.Number(2).pow(11).int();

// var qa = cloudyImage.select('QA60')
// Map.addLayer(qa.bitwiseAnd(cloudBitMask).neq(0), {}, 'clouds');
// Map.addLayer(qa.bitwiseAnd(cirrusBitMask).neq(0), {}, 'cirrus');

function maskS2clouds(image) {
    var qa = image.select('QA60');
    // Both flags should be set to zero, indicating clear conditions.
    var mask = qa.bitwiseAnd(cloudBitMask).eq(0).and(
        qa.bitwiseAnd(cirrusBitMask).eq(0));
    return image.updateMask(mask);
}

var cloudMasked = s2.filterBounds(GuangzhouP).map(maskS2clouds);

var median = cloudMasked.median().clip(GuangzhouP);
var bandnames = median.bandNames().remove('B10')
var qaimg = maskS2clouds(cloudyImage).select(bandnames).float()
// Map.addLayer(qaimg, visParamsRGB, 'qaimg')
print(qaimg)
var minImg = ee.ImageCollection([qaimg, median.select(bandnames)]).min()
// Map.addLayer(minImg, visParamsRGB, 'MinImg');
Map.addLayer(median, visParamsRGB, 'median');

Export.image.toAsset({
    image: median,
    description: 'Guangzhou',
    assetId: 'XGuangzhouImg',
    scale: 10,
    region: GuangzhouP,
});

// Export.image.toDrive({
//   image: median.select(['B2','B3','B4']),
//   description: 'XGuangzhou_B234',
//   scale: 10,
//   region: GuangzhouP,
//   maxPixels:1e13,
//   crs: 'EPSG:4326'
// });