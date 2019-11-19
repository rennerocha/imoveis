var baseLayer = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
  attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
  maxZoom: 20,
  id: 'mapbox.streets',
  accessToken: 'pk.eyJ1IjoicmVubmVyb2NoYSIsImEiOiJjajlveDRjNWgxaW9xMndudGZ1d25raXZ3In0.F5pLryFBNqKBOTfeZSkpJw'
})

var markers = L.markerClusterGroup();

$.getJSON("data.js", function (data) {
  var geojson = L.geoJson(data, {
    onEachFeature: function (feature, layer) {
      var props = feature.properties;

      var popup_content = '' +
        '<h4>' + props.code + ' </h4>' +
        '<table class="table table-striped table-sm">' +
        '  <tbody>' +
        '    <tr>' +
        '      <th scope="row">URL</th>' +
        '      <td><a href="' + props.url + '">anuncio</a></td>' +
        '    </tr>' +
        '    <tr>' +
        '      <th scope="row">Price</th>' +
        '      <td>R$ ' + props.rent_price + '</td>' +
        '    </tr>' +
        '    <tr>' +
        '      <th scope="row">Neighborhood</th>' +
        '      <td>R$ ' + props.neighborhood + '</td>' +
        '    </tr>' +
        '  </tbody>' +
        '</table>'

      layer.bindPopup(popup_content, {
        maxWidth: 500
      })
    }
  });

  markers.addLayer(geojson);
  var map = L.map('mapid', { maxZoom: 20 }).fitBounds(markers.getBounds()).setView([-22.8944129, -47.0798336], 11);
  baseLayer.addTo(map);
  markers.addTo(map);
});
