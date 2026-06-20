const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
let activeDow = null; // null = all days
let allFeatures = [];
let deckOverlay;

async function init() {
  const [geojson, meta] = await Promise.all([
    fetch("data/complaints.geojson").then(r => r.json()),
    fetch("data/meta.json").then(r => r.json()),
  ]);

  allFeatures = geojson.features;

  document.getElementById("meta").textContent =
    `${meta.record_count.toLocaleString()} complaints · updated ${meta.built_at.slice(0, 10)}`;

  const canvas = document.createElement("canvas");
  canvas.style.cssText = "position:absolute;top:0;left:0;width:100%;height:100%;";
  document.getElementById("map").appendChild(canvas);

  deckOverlay = new deck.Deck({
    canvas,
    initialViewState: INITIAL_VIEW,
    controller: true,
    layers: buildLayers(),
    onResize: ({width, height}) => { canvas.width = width; canvas.height = height; },
  });

  buildDowButtons();
}


function buildLayers() {
  const data = activeDow === null
    ? allFeatures
    : allFeatures.filter(f => f.properties.dow === activeDow);

  return [
    new deck.HexagonLayer({
      id: "noise-hex",
      data,
      getPosition: f => f.geometry.coordinates,
      radius: HEX_RADIUS,
      elevationScale: HEX_ELEVATION_SCALE,
      extruded: true,
      pickable: true,
      colorRange: [
        [255, 255, 178],
        [254, 204, 92],
        [253, 141, 60],
        [240, 59, 32],
        [189, 0, 38],
        [128, 0, 38],
      ],
    }),
  ];
}

function buildDowButtons() {
  const container = document.getElementById("dow-filter");
  const allBtn = document.createElement("button");
  allBtn.textContent = "All";
  allBtn.classList.add("active");
  allBtn.addEventListener("click", () => setDow(null, allBtn));
  container.appendChild(allBtn);

  DAYS.forEach((label, i) => {
    const btn = document.createElement("button");
    btn.textContent = label;
    btn.addEventListener("click", () => setDow(i, btn));
    container.appendChild(btn);
  });
}

function setDow(dow, activeBtn) {
  activeDow = dow;
  document.querySelectorAll("#dow-filter button").forEach(b => b.classList.remove("active"));
  activeBtn.classList.add("active");
  deckOverlay.setProps({ layers: buildLayers() });
}

init();
