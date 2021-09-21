var map;
const markers = [];

function initMap() {
    const myLatLng = { lat: 12.968331858875942, lng: 77.5952885571 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 12,
        center: myLatLng,
        mapId: '9cd3176a1f02dde6',
        disableDefaultUI: true
    });
    map.addListener('click', function (event) {
        console.log("click");
        placeMarker(event.latLng);
    });

    const contentString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        '<h1 id="firstHeading" class="firstHeading">Uluru</h1>' +
        '<div id="bodyContent">' +
        "<p><b>Uluru</b>, also referred to as <b>Ayers Rock</b>, is a large " +
        "sandstone rock formation in the southern part of the " +
        "Northern Territory, central Australia. It lies 335&#160;km (208&#160;mi) " +
        "south west of the nearest large town, Alice Springs; 450&#160;km " +
        "(280&#160;mi) by road. Kata Tjuta and Uluru are the two major " +
        "features of the Uluru - Kata Tjuta National Park. Uluru is " +
        "sacred to the Pitjantjatjara and Yankunytjatjara, the " +
        "Aboriginal people of the area. It has many springs, waterholes, " +
        "rock caves and ancient paintings. Uluru is listed as a World " +
        "Heritage Site.</p>" +
        '<p>Attribution: Uluru, <a href="https://en.wikipedia.org/w/index.php?title=Uluru&oldid=297882194">' +
        "https://en.wikipedia.org/w/index.php?title=Uluru</a> " +
        "(last visited June 22, 2009).</p>" +
        "</div>" +
        "</div>";
    const infowindow = new google.maps.InfoWindow({
        content: contentString
    });

    var kmlLayer = new google.maps.KmlLayer({
        url: 'https://raw.githubusercontent.com/romirk/scotland-yard/dev/public/map/mapdata.kml', //'https://googlearchive.github.io/js-v2-samples/ggeoxml/cta.kml',
        map: map
    });

    kmlLayer.addListener('click', function (kmlEvent) {
        var text = kmlEvent.featureData.description;
        console.log(kmlEvent);
        infowindow.setPosition(kmlEvent.latLng);
        infowindow.open({
            map,
            shouldFocus: false,
        });
    });

    function placeMarker(location) {
        var marker = new google.maps.Marker({
            position: location,
            map: map
        });
        markers.push(location);
    }
}

function placeAllMarkers() {

}
