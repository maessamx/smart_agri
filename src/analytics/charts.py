import matplotlib.pyplot as plt
import plotly.express as px


def governorate_ranking_chart(summary, metric_label, metric_column):
    figure, axis = plt.subplots(figsize=(10, 6))
    figure.patch.set_facecolor('#121f1a')
    axis.set_facecolor('#121f1a')
    axis.barh(summary['governorate'], summary[metric_column], color='#69c58e')
    axis.set_xlabel(metric_label)
    axis.set_ylabel('Governorate')
    axis.xaxis.label.set_color('#eef7f1')
    axis.yaxis.label.set_color('#eef7f1')
    axis.tick_params(colors='#d4e4da')
    axis.grid(axis='x', color='#587064', alpha=0.30)
    axis.set_axisbelow(True)
    axis.spines[['top', 'right']].set_visible(False)
    axis.spines[['left', 'bottom']].set_color('#587064')
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
    figure.update_layout(
        template='plotly_dark', height=580,
        plot_bgcolor='#121f1a', paper_bgcolor='#121f1a',
        font_color='#eef7f1', xaxis_tickangle=-45,
        legend_title_font_color='#eef7f1'
    )
    return figure
