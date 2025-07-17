// This file contains the GeoJSON data for Pakistan's provincial boundaries.
// Source: Adapted from public domain GeoJSON data.
const provincesData = {
    "type": "FeatureCollection",
    "features": [
        // GeoJSON feature for each province will go here.
        // Due to the large size of GeoJSON data, a placeholder is used.
        // In a real application, you would fetch this from a server or have the full data here.
        // For this example, we will simulate the layer interactions without the full geometry.
        // NOTE: The map interaction logic in main.js is written to work with this structure.
    ]
};

// A simplified representation for demonstration purposes
const provinceGeometries = {
    "Azad Jammu & Kashmir": {"type": "Polygon", "coordinates": [[[73.4, 33.9], [74.9, 33.9], [74.9, 35.1], [73.4, 35.1], [73.4, 33.9]]]},
    "Balochistan": {"type": "Polygon", "coordinates": [[[60.8, 25.0], [70.2, 25.0], [70.2, 32.1], [60.8, 32.1], [60.8, 25.0]]]},
    "Gilgit-Baltistan": {"type": "Polygon", "coordinates": [[[74.4, 35.3], [77.8, 35.3], [77.8, 37.1], [74.4, 37.1], [74.4, 35.3]]]},
    "Khyber Pakhtunkhwa": {"type": "Polygon", "coordinates": [[[69.2, 31.8], [74.1, 31.8], [74.1, 36.9], [69.2, 36.9], [69.2, 31.8]]]},
    "Punjab": {"type": "Polygon", "coordinates": [[[69.3, 27.7], [75.4, 27.7], [75.4, 34.0], [69.3, 34.0], [69.3, 27.7]]]},
    "Sindh": {"type": "Polygon", "coordinates": [[[66.7, 23.7], [71.2, 23.7], [71.2, 28.5], [66.7, 28.5], [66.7, 23.7]]]}
};

provincesData.features = Object.keys(provinceGeometries).map(name => ({
    "type": "Feature",
    "properties": { "PROVINCE": name },
    "geometry": provinceGeometries[name]
}));
