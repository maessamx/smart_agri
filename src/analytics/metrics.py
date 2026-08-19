METRICS = {
    'Cultivated Area': 'area_feddan',
    'Production': 'production_ton',
    'Yield': 'yield_ton_per_feddan'
}

def metric_column(label):
    return METRICS[label]
