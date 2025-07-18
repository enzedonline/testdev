// mapSettings should be similar structure to the below with max 25 waypoints
// {
//   uid: "id",
//   token: "your.mapbox.token",
//   style: "terrain", 
//   route_type: "walking",
//   show_route_info: true,
//   pitch: 50,
//   bearing: 120,
//   padding: {top: 5, right: 10, bottom: 5, left:10},
//   waypoints: [
//       {longitude: 11.77624, latitude": 42.1541, pin_label: "", show_pin: false},
//       {longitude: 12.128261, latitude": 42.168219, pin_label: "b", show_pin: true}
//   ]
// }
// Notes:
// style should be a key defined in the MapBlock.styles static object
// padding values are integers expressing padding as a percentage of the map, not pixels

class MapBlock {
    static colours = {
        start: '#02b875',
        end: '#d9534f',
        route: '#3887be'
    }

    static styles = {
        standard: "mapbox/standard",
        streets: "mapbox/streets-v12",
        terrain: "mapbox/outdoors-v12",
        satellite: "mapbox/standard-satellite",
        satellite_streets: "satellite-streets-v12"
    }

    static urls = {
        mapboxGlCSS: "https://api.tiles.mapbox.com/mapbox-gl-js/v3.8.0/mapbox-gl.css",
        mapboxGlJS: "https://api.tiles.mapbox.com/mapbox-gl-js/v3.8.0/mapbox-gl.js",
        threeD: "mapbox://mapbox.mapbox-terrain-dem-v1",
        directionsAPI: "https://api.mapbox.com/directions/v5/mapbox/"
    }

    constructor(uid) {
        include_css(MapBlock.urls.mapboxGlCSS);
        include_js(MapBlock.urls.mapboxGlJS)
            .then(() => {
                this.initialiseMap(uid);
            });
    }

    initialiseMap = (uid) => {
        this.blockContainer = document.getElementById(`mapblock-${uid}`);
        // read settings and dispose the json element
        const settingsElement = document.getElementById(uid);
        this.mapSettings = JSON.parse(settingsElement.textContent);
        // settingsElement.remove();
        // extract [lng, lat] from waypoint objects
        this.points = this.mapSettings.waypoints.map(
            waypoint => [waypoint.longitude, waypoint.latitude]
        );
        // calculate padding as px relative to map block container
        this.absolutePadding = {
            top: this.blockContainer.offsetHeight * this.mapSettings.padding.top / 100,
            right: this.blockContainer.offsetWidth * this.mapSettings.padding.right / 100,
            bottom: this.blockContainer.offsetHeight * this.mapSettings.padding.bottom / 100,
            left: this.blockContainer.offsetWidth * this.mapSettings.padding.left / 100
        };
        // create map
        this.add_mapbox();
        // add markers for any waypoints with 'show pin'
        this.addMarkers();
    }

    add_mapbox = () => {
        mapboxgl.accessToken = this.mapSettings.token;
        // get bounding box of waypoints
        const initialBounds = this.getBounds(this.points);
        // create base map object with camera options based on settings & bounds
        this.map = new mapboxgl.Map({
            container: `map-${this.mapSettings.uid}`,
            style: `mapbox://styles/${MapBlock.styles[this.mapSettings.style] ?? MapBlock.styles.terrain}`,
            bounds: initialBounds,
            fitBoundsOptions: {
                bearing: this.mapSettings.bearing,
                pitch: this.mapSettings.pitch,
                padding: { ...this.absolutePadding }
            }
        });
        // add compass, scale and full-screen controls
        this.map.addControl(new mapboxgl.NavigationControl({ visualizePitch: true }));
        this.map.addControl(new mapboxgl.ScaleControl({ position: "bottom-right" }));
        this.map.addControl(new mapboxgl.FullscreenControl());
        // add style load handler
        this.map.on('style.load', this.onStyleLoad);
    }

    onStyleLoad = async () => {
        // enable 3D & draw any routes whenever a style loads
        this.enable3D();
        // add route layer if relevant
        // custom layers must be re-added if style changes after loading
        if (!!this.mapSettings.route_type) {
            if (this['customLayers']) {
                // style changed, reload layers from cached values
                this.addCustomLayers();
            } else {
                // first run, fetch route data and fit bounds to container
                this.customLayers = [];
                await this.fetchRoute();
                this.addCustomLayers();
                if (this.mapSettings.show_route_info) {
                    this.showRouteInfo();
                }
                // set map bounds to fit route
                const bounds = this.getBounds(this.routeData.geometry.coordinates);
                this.fitBoundsToContainer(bounds, this.mapSettings.bearing, this.mapSettings.pitch);
            }
        }
    }

    addCustomLayers = async () => {
        // add all the layers in the customLayers array to the map
        this.customLayers.forEach(layer => {
            this.map.addLayer(layer);
        });
    }

    enable3D = async () => {
        // add the DEM source as a terrain layer with exaggerated height
        this.map.addSource('mapbox-dem', {
            'type': 'raster-dem',
            'url': MapBlock.urls.threeD
        });
        this.map.setTerrain({ 'source': 'mapbox-dem', 'exaggeration': 1.5 });
    }

    addMarkers = async () => {
        // add markers with Google Maps links
        const showRoute = (!!this.mapSettings.route_type)
        for (let i = 0; i < this.mapSettings.waypoints.length; i++) {
            const waypoint = this.mapSettings.waypoints[i];
            // if showing route, set first and last marker colours
            let config = {};
            if (showRoute) {
                if (i === 0) {
                    config = { color: MapBlock.colours.start }
                } else if (i === (this.mapSettings.waypoints.length - 1)) {
                    config = { color: MapBlock.colours.end }
                }
            }
            if (waypoint.show_pin) {
                // add pin with any label and link to Google Maps for location
                let waypointLabel = waypoint.pin_label ? `<b>${waypoint.pin_label}</b><br>` : '';
                waypointLabel += `<a href="https://www.google.com/maps?q=${waypoint.latitude},${waypoint.longitude}" 
                    target="_blank" class="map-block-waypoint-link">${waypoint.latitude}, ${waypoint.longitude}</a>`;
                const popup = new mapboxgl.Popup().setHTML(waypointLabel);
                new mapboxgl.Marker(config)
                    .setLngLat([waypoint.longitude, waypoint.latitude])
                    .setPopup(popup)
                    .addTo(this.map);
            }
        };
    }

    fetchRoute = async () => {
        // build the gps points query string
        const points = this.mapSettings.waypoints.map((coord) => [coord.longitude, coord.latitude].join()).join(";");
        // get directions API response - set steps=true to return data on each route leg
        const query = await fetch(
            `${MapBlock.urls.directionsAPI}${this.mapSettings.route_type}/${points}?steps=false&geometries=geojson&access_token=${mapboxgl.accessToken}`,
            { method: "GET" }
        );
        // return if api call not successful
        if (!query.ok) {
            console.warn("Map Block: Error determining route");
            return
        }
        // read body stream
        const json = await query.json();
        // routes is an array, no alternatives requested, array has ony one member
        // routeData used to display route information (distance, duration etc)
        this.routeData = json.routes[0];
        const geojson = {
            type: "Feature",
            properties: {},
            geometry: {
                type: "LineString",
                coordinates: this.routeData.geometry.coordinates,
            },
        };
        // add layer configs to customLayers array
        this.customLayers.push(this.getRouteLayerConfig(geojson));
        this.customLayers.push(this.getEndpointLayerConfig('start', this.mapSettings.waypoints[0], MapBlock.colours.start));
        this.customLayers.push(this.getEndpointLayerConfig('end', this.mapSettings.waypoints.at(-1), MapBlock.colours.end));
    }

    showRouteInfo = () => {
        // show route length info on page
        const distanceElement = this.blockContainer.querySelector(`#distance-${this.mapSettings.uid}`);
        const routeSummaryElement = this.blockContainer.querySelector(`#routesummary-${this.mapSettings.uid}`);
        distanceElement.innerText = (this.routeData.distance / 1000).toFixed(1);
        routeSummaryElement.style.display = "block";
        // Uncomment to include duration stats (displayed in hours)
        // const durationElement = this.blockContainer.querySelector(`#hours-${this.mapSettings.uid}`);
        // durationElement.innerText = (data.duration / 360).toFixed(1);
    }

    getRouteLayerConfig = (geojson) => {
        return {
            id: `route-${this.mapSettings.uid}`,
            type: "line",
            metadata: { route: true },
            source: {
                type: "geojson",
                data: geojson,
            },
            layout: {
                "line-join": "round",
                "line-cap": "round",
            },
            paint: {
                "line-color": MapBlock.colours.route,
                "line-width": 5,
                "line-opacity": 0.75,
            },
        }
    }

    getEndpointLayerConfig = (id, waypoint, color) => {
        return {
            id: `${id}-${this.mapSettings.uid}`,
            type: "circle",
            metadata: { route: true },
            source: {
                type: "geojson",
                data: {
                    type: "FeatureCollection",
                    features: [
                        {
                            type: "Feature",
                            properties: {},
                            geometry: {
                                type: "Point",
                                coordinates: [
                                    waypoint.longitude,
                                    waypoint.latitude,
                                ],
                            },
                        },
                    ],
                },
            },
            paint: {
                "circle-radius": 10,
                "circle-color": color,
            },
        };
    }

    getBounds = (points) => {
        // get the bounding box for the waypoints (as LngLatBounds)
        if (this.mapSettings.bearing === 0) {
            return this.findBoundingBox(points);
        } else {
            return this.findRotatedBoundingBox(points, this.mapSettings.bearing);
        }
    }

    // get bounding box from points array - use only if bearing===0
    // IN: [[lng, lat], [lng, lat] ...]
    // OUT: bounds object
    findBoundingBox = (points) => {
        const { swX, neX, swY, neY } = points.reduce(
            (acc, [x, y]) => ({
                swX: Math.min(acc.swX, x),
                neX: Math.max(acc.neX, x),
                swY: Math.min(acc.swY, y),
                neY: Math.max(acc.neY, y),
            }),
            { swX: Infinity, neX: -Infinity, swY: Infinity, neY: -Infinity }
        );
        return new mapboxgl.LngLatBounds([[swX, swY], [neX, neY]])
    }

    // find a bounding box for any rotated set of points
    findRotatedBoundingBox = (points, bearing) => {
        // convert degrees to radians
        const toRadians = (degrees) => (degrees * Math.PI) / 180;
        // Rotate a point [lng, lat] around a given origin by an angle in radians
        const rotatePoint = ([lng, lat], angle, origin) => {
            const cosTheta = Math.cos(angle);
            const sinTheta = Math.sin(angle);
            const translatedLng = lng - origin[0];
            const translatedLat = lat - origin[1];
            const xRot = translatedLng * cosTheta - translatedLat * sinTheta;
            const yRot = translatedLng * sinTheta + translatedLat * cosTheta;
            return [xRot, yRot];
        }
        // Find centroid from an array of points
        const findCentroid = (points) => {
            return points.reduce(
                ([sumLng, sumLat], [lng, lat]) => [sumLng + lng, sumLat + lat],
                [0, 0]
            ).map((sum) => sum / points.length);
        }
        const bearingRadians = toRadians(bearing);
        const centroid = findCentroid(points);
        // Rotate all points to the rotated coordinate space using the centroid
        const rotatedPoints = points.map((point) => rotatePoint(point, bearingRadians, centroid));
        // Find bounding box in rotated space
        const rotatedBounds = this.findBoundingBox(rotatedPoints).toArray();
        // Rotate the bounding box corners back to the original space
        const bounds = rotatedBounds.map(
            (corner) => rotatePoint(corner, -bearingRadians, [0, 0]) // Unrotate without centering
        ).map(
            ([lng, lat]) => [lng + centroid[0], lat + centroid[1]]
        );
        return new mapboxgl.LngLatBounds(bounds);
    }

    fitBoundsToContainer = (bounds, bearing, pitch) => {
        // cancel any running animations
        this.map.stop();
        // get camera bounds given bounding box, pitch and bearing
        const cameraBounds = this.map.cameraForBounds(bounds, {
            padding: 0,
            pitch: pitch,
            bearing: bearing
        });
        // Get the map's container dimensions
        const container = this.map.getContainer();
        const containerWidth = container.offsetWidth - this.absolutePadding.left - this.absolutePadding.right;
        const containerHeight = container.offsetHeight - this.absolutePadding.top - this.absolutePadding.bottom;
        // Get bounding box dimensions in px
        const sw = this.map.project(bounds.getSouthWest());
        const ne = this.map.project(bounds.getNorthEast());
        const bboxWidth = Math.abs(sw.x - ne.x);
        const bboxHeight = Math.abs(sw.y - ne.y);
        // calculate optimal zoom
        const scaleWidth = containerWidth / bboxWidth;
        const scaleHeight = containerHeight / bboxHeight;
        const scale = Math.min(scaleWidth, scaleHeight);
        const optimalZoom = this.map.getZoom() + Math.log2(scale)
        // calculate offset in case padding uneven in either direction
        let offset = null;
        if (
            (this.absolutePadding.left !== this.absolutePadding.right) ||
            (this.absolutePadding.top !== this.absolutePadding.bottom)
        ) {
            offset = [
                this.absolutePadding.right - this.absolutePadding.left,
                this.absolutePadding.bottom - this.absolutePadding.top
            ]
        }
        // pan map to camera bounds then apply any padding offset
        this.map.easeTo({
            ...cameraBounds,
            padding: 0,
            zoom: optimalZoom,
            duration: 1000
        });
        if (offset) {
            this.map.once('moveend', () => {
                this.map.panBy(offset, {
                    duration: 1000
                });

            });
        }
    }
}