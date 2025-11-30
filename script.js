var map = L.map('map', { preferCanvas: true }).setView([50.45, 30.52], 12);

L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
  maxZoom: 20,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

function getColor(s) {
    return s == 3 ? '#808080ff' :
           s == 2 ? '#800000ff' :
                    '#008000ff' ;
}

function style(feature) {
    return {
        stroke: false,
        fillColor: '#00a500ff',
        fillOpacity: 0.7
    };
}

L.geoJson(kyiv_districts, {style: style}).addTo(map)
