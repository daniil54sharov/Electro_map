var map = L.map('map', { preferCanvas: true }).setView([50.45, 30.52], 12);

L.tileLayer('https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png', {
  maxZoom: 20,
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

function getColor(s) {
    return s >= 4.4 ? '#808080ff' :
           s >= 2.2 ? '#800000ff' :
                    '#008000ff' ;
}

function style(feature) {
    const props = feature.properties || {};

    // Проверяем наличие всех трёх полей yasno
    const hasAllYasno =
        props.yasnoStreetData &&
        props.yasnoHouseData &&
        props.yasnoGroupData;

    const hasAddress =
        props["addr:street"] &&
        props["addr:housenumber"];

    let color;

    if (!hasAddress) {
        color = '#808080'; // серый
    } else if (hasAddress && !hasAllYasno) {
        color = '#aa0000'; // красный
    } else if (hasAddress && hasAllYasno) {
        color = '#00aa00'; // зеленый
    }

    return {
        stroke: false,
        fillColor: color,
        fillOpacity: 0.7
    };
}

// Функция для показа popup при клике — выводит только нужные поля, если они есть
function onEachFeature(feature, layer) {
    const p = feature.properties || {};

    // Собираем нужные поля, но показываем только существующие
    const addrStreet = p["addr:street"];
    const addrHn = p["addr:housenumber"];

    const yasnoStreet = p.yasnoStreetData?.value;
    const yasnoStreetId = p.yasnoStreetData?.id;
    const yasnoHouse = p.yasnoHouseData?.value;
    const yasnoHouseId = p.yasnoHouseData?.id;
    const yasnoGroup = p.yasnoGroupData?.value;
    const yasnoGroupGroup = p.yasnoGroupData?.group;
    const yasnoGroupSubgroup = p.yasnoGroupData?.subgroup;

    // Формируем HTML содержимое popup
    let html = '<div style="font-family: monospace; white-space: pre-wrap;">';

    // Адрес (если есть)
    if (addrStreet || addrHn) {
        html += `<b>Адрес:</b>\n`;
        html += `  ${addrStreet ?? '—'}`;
        if (addrHn) html += `, ${addrHn}`;
        html += `\n\n`;
    } else {
        html += `<b>Адрес:</b> —\n\n`;
    }

    // yasnoStreetData
    if (yasnoStreet || yasnoStreetId !== undefined) {
        html += `<b>yasnoStreetData:</b>\n`;
        html += `  id: ${yasnoStreetId ?? '—'}\n`;
        html += `  value: ${yasnoStreet ?? '—'}\n\n`;
    }

    // yasnoHouseData
    if (yasnoHouse || yasnoHouseId !== undefined) {
        html += `<b>yasnoHouseData:</b>\n`;
        html += `  id: ${yasnoHouseId ?? '—'}\n`;
        html += `  value: ${yasnoHouse ?? '—'}\n\n`;
    }

    // yasnoGroupData
    if (yasnoGroup || yasnoGroupGroup !== undefined || yasnoGroupSubgroup !== undefined) {
        html += `<b>yasnoGroupData:</b>\n`;
        html += `  group: ${yasnoGroupGroup ?? '—'}\n`;
        html += `  subgroup: ${yasnoGroupSubgroup ?? '—'}\n`;
        html += `  value: ${yasnoGroup ?? '—'}\n\n`;
    }

    html += '</div>';

    // Если есть хотя бы что-то, привяжем popup; иначе можно всё равно привязать минимальный popup
    layer.bindPopup(html, { maxWidth: 400 });
}

fetch('kyiv_districts.GeoJSON')
  .then(resp => {
    if (!resp.ok) throw new Error(resp.statusText);
    return resp.json();
  })
  .then(data => {
    L.geoJSON(data, {
      style: style,
      onEachFeature: onEachFeature
    }).addTo(map);
  })
  .catch(err => console.error('Ошибка загрузки geojson:', err));
