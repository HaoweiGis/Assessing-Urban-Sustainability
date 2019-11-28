/*
 * @Author: Muhaowei
 * @Date: 2019-11-28 17:34:29
 * @LastEditors: Muhaowei
 * @LastEditTime: 2019-11-28 17:40:04
 * @Description: 
 */
var mcd12q1 = ee.ImageCollection("MODIS/006/MCD12Q1"),
    mod17a2h = ee.ImageCollection("MODIS/006/MOD17A2H"),
    guangzhoup = ee.FeatureCollection("users/blackmhw/Guangzhou/GuangzhouP"),
    guangdong = ee.FeatureCollection("users/blackmhw/Guangzhou/guangdong"),
    GuangzhouCity = ee.FeatureCollection("users/blackmhw/Guangzhou/GuangzhouCity");

Map.addLayer(GuangzhouCity)
var China = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017').filter(ee.Filter.eq('country_na', 'China'))
// Map.addLayer(China)
var landcover_china = ee.Image('MODIS/006/MCD12Q1/2018_01_01').select("LC_Type1").clip(China)
// print(landcover)

var y2018 = mod17a2h.filterDate('2019-01-01', '2019-09-20').filterBounds(China)
print(y2018)
// '2018-07-27','2018-08-22'
var y2018_month = mod17a2h.filterDate('2019-05-01', '2019-09-20').filterBounds(GuangzhouCity)
print(y2018_month)

var SelectBand = function (y2018) {
    return y2018.select('PsnNet')
};

var y2018_PsnNet = y2018.map(SelectBand)
var y2018_month_PsnNet = y2018_month.map(SelectBand)

var Trees_China_mask = landcover_china.eq(10)
// var Trees_China_mask = landcover_china.eq(2)
var Trees_Guangzhou_mask = Trees_China_mask.clip(GuangzhouCity)

var y2018_PsnNet_China_year = y2018_PsnNet.sum().clip(China).updateMask(Trees_China_mask).divide(256)
var y2018_PsnNet_Guangzhou_month = y2018_month_PsnNet.sum().clip(GuangzhouCity).updateMask(Trees_Guangzhou_mask).divide(136)
// Map.addLayer(y2018_PsnNet_Guangzhou_month,{},'y2018_PsnNet_Guangzhou_month')
// Map.addLayer(y2018_PsnNet_China_year,{},'y2018_PsnNet_China_year')


var Chinasum = y2018_PsnNet_China_year.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: China,
    scale: 500,
    maxPixels: 1e9
});
print(Chinasum)
var Chinacount = y2018_PsnNet_China_year.reduceRegion({
    reducer: ee.Reducer.count(),
    geometry: China,
    scale: 500,
    maxPixels: 1e9
});

print(Chinacount)

var Guangzhousum = y2018_PsnNet_Guangzhou_month.reduceRegion({
    reducer: ee.Reducer.sum(),
    geometry: GuangzhouCity,
    scale: 500,
    maxPixels: 1e9
});
print(Guangzhousum)
var Guangzhoucount = y2018_PsnNet_Guangzhou_month.reduceRegion({
    reducer: ee.Reducer.count(),
    geometry: GuangzhouCity,
    scale: 500,
    maxPixels: 1e9
});
print(Guangzhoucount)
