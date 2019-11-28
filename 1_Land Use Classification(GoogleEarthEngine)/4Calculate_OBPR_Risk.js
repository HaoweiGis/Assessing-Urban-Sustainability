/*
 * @Author: Muhaowei
 * @Date: 2019-11-28 17:34:29
 * @LastEditors: Muhaowei
 * @LastEditTime: 2019-11-28 18:04:39
 * @Description: 
 */

var Pclassified_RF = ee.Image("users/blackmhw/PclassifiedGZ"),
    SegObject = ee.FeatureCollection("users/blackmhw/SegGuangzhou_Clip"),
    Oclassified_RF = ee.Image("users/blackmhw/OclassifiedGZ"),
    TrafficA1 = ee.FeatureCollection("users/blackmhw/Guangzhou_TrafficA1"),
    table = ee.FeatureCollection("users/blackmhw/GuangzhouP");

Export.image.toDrive({
    image: Oclassified_RF,
    description: 'Oclassified_RF_vaildation',
    scale: 10,
    region: table,
    maxPixels: 1e13,
    crs: 'EPSG:4326'
});

var VectorToRaster = function (Features, value) {
    var Image = Features
        // .filter(ee.Filter.notNull(['Area_Pxl']))
        .reduceToImage({
            properties: [value],
            reducer: ee.Reducer.first()
        });
    return Image
};

Map.addLayer(SegObject)
Map.addLayer(TrafficA1)
Map.centerObject(TrafficA)
Map.addLayer(Oclassified_RF)
Map.addLayer(Pclassified_RF)

var modeFeatures = Pclassified_RF.reduceRegions({
    collection: SegObject,
    reducer: ee.Reducer.mode(),
    scale: 10,
});
var Pclassified_RF0 = Pclassified_RF.eq(0)
var Pclassified_RF0M = Pclassified_RF.updateMask(Pclassified_RF0)
Map.addLayer(Pclassified_RF)
Map.addLayer(Pclassified_RF0)
Map.addLayer(Pclassified_RF0M)

var modeFeatures0 = Pclassified_RF.reduceRegions({
    collection: SegObject,
    reducer: ee.Reducer.mode(),
    // reducer: ee.Reducer.frequencyHistogram(),
    scale: 10,
});
// print(modeFeatures0.filter.first())

// var OmodeFeatures = Oclassified_RF.reduceRegions({
//   collection: TrafficA1,
//   reducer: ee.Reducer.frequencyHistogram(),
//   scale: 10,
// });
// print(OmodeFeatures)
// Map.addLayer(OmodeFeatures)

Export.table.toDrive({
    collection: modeFeatures0,
    description: 'OmodeFeature',
    fileFormat: 'KML'
});

Export.table.toDrive({
    collection: OmodeFeatures,
    description: 'TmodeFeatures1',
    fileFormat: 'csv'
});

var modeImg = VectorToRaster(modeFeatures, 'mode').int().select(['first'], ['mode'])
Map.addLayer(modeImg, { min: 0, max: 7, palette: igbpPalette },
    'modeImg');



var validation = modeImg.sampleRegions({
    collection: sample_validate,
    properties: ["CLASSIFIED"],
    scale: 10,
    geometries: true
});
print(sample_validate)
print(validation)

var valacc = validation.errorMatrix('land_use', 'mode')
var valkappa = valacc.kappa()
var CATrain = valacc.consumersAccuracy()
var PATrain = valacc.producersAccuracy()
var AllTain = valacc.accuracy()
print(valacc, valkappa)


var OResultF = ee.FeatureCollection([
    // ee.Feature(null,{name: 'TrainingData',acc:OtrainAccuracy,kappa:OkappaTrain}),
    ee.Feature(null, { name: 'TestData', kappa: valkappa, CA: CATrain, PA: PATrain, All: AllTain })
]);
Export.table.toDrive({
    collection: OResultF,
    description: 'ObjectResult',
    fileFormat: 'CSV'
});
exportTable(valacc, 'ObjectAccuracy')