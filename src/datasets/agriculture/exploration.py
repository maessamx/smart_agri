from .preprocessing import clean_agriculture_data


def agriculture_overview(data=None):
    data = clean_agriculture_data() if data is None else data
    return {
        'records': len(data),
        'governorates': data['governorate'].nunique(),
        'products': data['product'].nunique(),
        'categories': data['product_category'].nunique(),
        'missing_values': data.isna().sum().to_dict()
    }


def product_summary(data, product, metric):
    subset = data[data['product'].eq(product)].dropna(subset=[metric]).copy()
    return subset.groupby('governorate', as_index=False)[metric].sum().sort_values(metric, ascending=False)
