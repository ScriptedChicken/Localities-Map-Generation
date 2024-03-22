localities = QgsProject.instance().mapLayersByName('localities')[0]
localities_inactive = QgsProject.instance().mapLayersByName('localities inactive')[0]

canvas = iface.mapCanvas()

ids = [ftr['id'] for ftr in localities.getFeatures()]
id_count = len(ids)

for i, id in enumerate(ids):
    localities.setSubsetString(f"id = {id}")
    localities_inactive.setSubsetString(f"id <> {id}")
    
    extent = localities.extent()
    canvas.setExtent(extent)
    canvas.refresh()
    
    manager = QgsProject.instance().layoutManager()
    homePath = QgsProject.instance().homePath()
    layout = manager.layoutByName("layout")
    
    for ftr in localities.getFeatures():
        layout.itemById('Title').setText(ftr["name"])
        population_estimate = ftr['population_estimate']
        if population_estimate:
            population_estimate = int(population_estimate)
        locality_type = ftr['type']
        details_text = f"Population Estimate: {population_estimate}\nType: {locality_type}"
        layout.itemById('Details').setText(details_text)
        
    map_frame = layout.itemById('Map Frame')
    map_frame.zoomToExtent(canvas.extent())
    exporter = QgsLayoutExporter(layout)
    name_clean = ftr["name"].replace(r'/','')
    exporter_path = os.path.join(homePath, 'Outputs', f'{name_clean}.png')
    exporter.exportToImage(exporter_path, QgsLayoutExporter.ImageExportSettings())
    
    print(f"Exported {exporter_path} ({i} / {id_count})", end='\r')
    
    if i > 100:
        break
    
localities.setSubsetString(None)
print("Completed")