import matplotlib.pyplot as plt
import plotly.express as px


def governorate_ranking_chart(summary, metric_label, metric_column):
    figure, axis = plt.subplots(figsize=(10, 6))
    axis.barh(summary['governorate'], summary[metric_column], color='#25734D')
    axis.set_xlabel(metric_label)
    axis.set_ylabel('Governorate') 
    axis.grid(axis='x', alpha=0.18)
    axis.spines[['top', 'right']].set_visible(False)
    figure.tight_layout()
    return figure


def stacked_category_chart(data, metric_label, metric_column):
    grouped = data.groupby(['governorate', 'product_category'], as_index=False)[metric_column].sum()
    figure = px.bar(
        grouped,
        x='governorate',
        y=metric_column,
        color='product_category',
        barmode='stack',
        color_discrete_sequence=px.colors.qualitative.Set2,
        labels={
            'governorate': 'Governorate',
            'product_category': 'Product Category',
            metric_column: metric_label
        }
    )
    figure.update_layout(height=580, plot_bgcolor='white', paper_bgcolor='white', xaxis_tickangle=-45)
    return figure
