import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

from vars import *

custom_layout = {
    'plot_bgcolor': '#4e5567',
    'paper_bgcolor': '#2b323f',
    'font': {'color': 'white'},
    'legend': {'bgcolor': '#2b323f'},
    'xaxis': {
        'title_font': {'color': 'white'},
        'tickfont': {'color': 'white'},
        'gridcolor': 'darkgrey'
    },
    'yaxis': {
        'title_font': {'color': 'white'},
        'tickfont': {'color': 'white'},
        'gridcolor': 'darkgrey'
    }
}


def plot_stability_plotly(variable):
    stability_df = dataprep.train.groupby([dataprep.date, variable])[dataprep.target].mean().unstack()

    fig = go.Figure()

    for i, class_label in enumerate(stability_df.columns):
        values = stability_df[class_label]
        fig.add_trace(go.Scatter(x=stability_df.index,
                                 y=values,
                                 mode='lines+markers',
                                 name=f'Classe {class_label}'))

    fig.update_layout(title=f'Stabilité temporelle de {variable}',
                      xaxis_title='Date',
                      yaxis_title='Proportion de la cible',
                      legend_title='Classes',
                      margin=dict(l=20, r=20, t=40, b=20),
                      height = 500)

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="top",
        y=-0.2,
        xanchor="center",
        x=0.5
    ))
    fig.update_layout(**custom_layout)

    return fig

def plot_hist(column):
    histogramme = go.Figure(go.Histogram(x=dataprep.train[column]))

    histogramme.update_layout(
        title=f'Distribution de {column}',
        xaxis_title=column,
        yaxis_title='Fréquence',
        bargap=0.2,
        height=520
    )

    histogramme.update_layout(**custom_layout)

    return histogramme

def courbe_roc(model):
    metrics = model.get_metrics()
    fpr = metrics["fpr"]
    tpr = metrics["tpr"]
    roc_auc = metrics["roc_auc"]

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=fpr,
                             y=tpr,
                             mode='lines',
                             name='Courbe ROC (AUC = {:.2f})'.format(roc_auc),
                             line=dict(width=4)))

    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1],
                             mode='lines',
                             name='Chance',
                             line=dict(width=2, dash='dash')))

    fig.update_layout(title='Courbe ROC',
                      xaxis_title='Taux Faux Positifs',
                      yaxis_title='Taux Vrais Positifs',
                      legend=dict(y=0.01, x=0.99, xanchor='right', yanchor='bottom'),
                      margin=dict(l=40, r=0, t=40, b=30))

    fig.update_layout(**custom_layout)

    return(fig)

def gini_coefficient(values):
    sorted_values = np.sort(values)
    n = len(values)
    cumulative_values_sum = np.cumsum(sorted_values)
    gini_index = (2 * np.sum(cumulative_values_sum) / (n * np.sum(sorted_values))) - (n + 1) / n
    return 1 - gini_index

def create_gini_figure(model):
    df = model.df_score.copy()
    if "date_trimestrielle" not in df.columns :
        df[dataprep.date] = pd.to_datetime(df[dataprep.date])
        df['date_trimestrielle'] = df[dataprep.date].dt.year.astype(str) + '_' + df[dataprep.date].dt.quarter.astype(str)

    fig = go.Figure()
    for classe in range(1, 8):
        df_classe = df[df['Classes'] == classe][["date_trimestrielle", dataprep.target]]
        grouped = df_classe.groupby(df_classe['date_trimestrielle'])[dataprep.target]
        gini_per_year = grouped.apply(gini_coefficient)

        fig.add_trace(go.Scatter(x=gini_per_year.index, y=gini_per_year, mode='lines+markers',
                                 name=f'Classe {classe}'))

    fig.update_layout(title='Évolution Temporelle du Coefficient de Gini par Classe Homogène de Risque',
                      xaxis_title='Date',
                      yaxis_title='Coefficient de Gini',
                      legend_title='Classe',
                      template='plotly_white')

    fig.update_layout(xaxis=dict(tickangle=-45))

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    fig.update_layout(**custom_layout)

    return fig



def create_stability_figure(model):
    df = model.df_score.copy()
    if "date_trimestrielle" not in df.columns :
        df[dataprep.date] = pd.to_datetime(df[dataprep.date])
        df['date_trimestrielle'] = df[dataprep.date].dt.year.astype(str) + '_' + df[dataprep.date].dt.quarter.astype(str)

    fig = go.Figure()
    stability_df = df.groupby(['date_trimestrielle', 'Classes'])[dataprep.target].mean().unstack()

    for class_label in stability_df.columns:
        values = stability_df[class_label]
        fig.add_trace(go.Scatter(x=stability_df.index,
                                 y=values,
                                 mode='lines+markers',
                                 name=f'Classe {class_label}'))

    fig.update_layout(title=f'Stabilité temporelle des Classes Homogènes de Risque',
                      xaxis_title='Date',
                      yaxis_title='Proportion de la cible',
                      legend_title=f'Classes',
                      template='plotly_white')

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    fig.update_layout(xaxis=dict(tickangle=-45))
    fig.update_layout(**custom_layout)

    return fig

def plot_shap_values():
    if model_challenger.model_name == "xgb" :
        shap_values = model_challenger.model.shap_values
        train = model_challenger.model.X_train

        shap_values = pd.DataFrame(shap_values, columns=train.columns)
        train.reset_index(inplace=True, drop=True)

        replacements = {
            'zz': '[',
            'vv': ']',
            'ww': ';',
            'ff': '-',
            'pp': '.'
        }

        for old, new in replacements.items():
            train.columns = [col.replace(old, new) for col in train.columns]
            shap_values.columns = [col.replace(old, new) for col in shap_values.columns]

        train = train.iloc[:500, :]
        shap_values = shap_values.iloc[:500, :]

        # Joining SHAP values and one-hot encoded features
        merged_df = shap_values.join(train, lsuffix='_shap', rsuffix='_train')

        # Melt the merged DataFrame to long format
        melted_df = merged_df.melt(value_vars=[col for col in
                                               merged_df.columns if '_shap' in col],
                                   var_name='Feature',
                                   value_name='SHAP Value')

        melted_df['Feature'] = melted_df['Feature'].str.replace('_shap', '')

        for feature in train.columns:
            feature_shap = feature + '_shap'
            feature_train = feature + '_train'
            melted_df.loc[melted_df['Feature'] == feature, 'One-hot Value'] = merged_df[feature_train].values

        # Generate the plot again
        fig = px.strip(melted_df, x='SHAP Value', y='Feature',
                       color='One-hot Value',
                       orientation='h', stripmode='overlay',
                       title='Impact des Variables sur la sortie du modèle')

        fig.update_layout(xaxis_title='Valeurs de Shapley',
                          yaxis_title='Variable')

        fig.update_layout(**custom_layout)

        return(fig)


def plot_metrics_leftpanel(metrics) :
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=[metrics],
        y=[metrics],
        text=[f'{round(metrics)}%'],
        textposition='auto',
        orientation='h',
    ))

    fig.update_layout(
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[0, 100]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        height=40,

    )
    fig.update_layout(**custom_layout)

    fig.update_layout(paper_bgcolor = '#4e5567')

    return(fig)

def update_graph_dist_column(selected_column, model):
    default = model.df_score[model.df_score[dataprep.target] == 1][selected_column]
    not_default = model.df_score[model.df_score[dataprep.target] == 0][selected_column]

    column_data_type = default.dtype

    if column_data_type in ['int64', 'float64']:

        fig = ff.create_distplot(hist_data=[default, not_default],
                                 group_labels=['Défaut', 'Non Défaut'],
                                 bin_size=0.2,
                                 show_rug=False,
                                 show_hist=False)

        fig.update_layout(title=f'Distribution conditionnelle au défaut de la variable {selected_column}')
        fig.update_traces(fill='tozeroy')
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))
        fig.update_layout(**custom_layout)

    else:
        categories = sorted(set(default.unique()))
        fig = go.Figure()

        fig.add_trace(go.Histogram(x=default,
                                   nbinsx=len(categories),
                                   name='Défaut',
                                   opacity=0.7))

        fig.add_trace(go.Histogram(x=not_default,
                                   nbinsx=len(categories),
                                   name='Non Défaut',
                                   opacity=0.7))
        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))

        fig.update_layout(title=f'Distribution conditionnelle au défaut de la variable {selected_column}')
        fig.update_layout(**custom_layout)

    return fig

def proba_defaut(grouped):
    fig = go.Figure()
    grouped["Classes"] = range(1,grouped.shape[0]+1)
    grouped["MOC_C"] = grouped["Moc_C"]

    grouped['Proba_Defaut'] = grouped['LRA'] + grouped['MOC_A'] + grouped['MOC_C']


    for component in ['LRA', 'MOC_A', 'MOC_C']:
        fig.add_trace(go.Bar(
            x=grouped['Classes'],
            y=grouped[component],
            name=component,
        ))

    annotations = []
    for i, proba in zip(grouped['Classes'], grouped['Proba_Defaut']):
        annotations.append(dict(
            x=i, y=proba, text=str(round(proba,2)), xanchor='center', yanchor='bottom', showarrow=False
        ))

    # Mise en page du graphique
    fig.update_layout(
        barmode='stack',  # Mode empilé
        title='Probabilité de défaut par classe',
        xaxis_title='Classes',
        yaxis_title='Probabilité de défaut',
        annotations = annotations,
    )

    fig.update_layout(**custom_layout)
    fig.update_layout(
        height=600,
    )
    return(fig)

def compare_PD():
    default_proba_avant = model_classique.default_proba_before
    default_proba_apres = model_classique.default_proba

    classes = default_proba_avant['Classe']
    prob_avant = default_proba_avant['Probabilité_Défaut']
    prob_apres = default_proba_apres['Probabilité_Défaut']

    diff_prob = [p2 - p1 for p1, p2 in zip(prob_avant, prob_apres)]

    trace_avant = go.Bar(x=classes, y=prob_avant, name='Avant')
    trace_apres = go.Bar(x=classes, y=prob_apres, name='Après')
    trace_diff = go.Bar(x=classes, y=diff_prob, name='Différence')

    fig = go.Figure(data=[trace_avant, trace_apres, trace_diff])

    fig.update_layout(
        xaxis=dict(title='Classe'),
        yaxis=dict(title='Probabilité de Défaut'),
        barmode='group',
        margin=dict(l=0, r=0, t=10, b=0)
    )

    fig.update_layout(**custom_layout)

    return(fig)

def compare_monotonie():
    default_proba_avant = model_classique.default_proba_before
    default_proba_apres = model_classique.default_proba

    classes = default_proba_avant['Classe']
    prob_avant = default_proba_avant['Probabilité_Défaut']
    prob_apres = default_proba_apres['Probabilité_Défaut']

    trace_avant = go.Scatter(x=classes, y=prob_avant, mode='lines+markers', name='Avant', line=dict(color='blue'))
    trace_apres = go.Scatter(x=classes, y=prob_apres, mode='lines+markers', name='Après', line=dict(color='red'))

    fig1 = go.Figure(data=[trace_avant, trace_apres])
    fig1.update_layout(margin=dict(l=0, r=0, t=10, b=0),
                       xaxis_title='Classe',
                       yaxis_title='Probabilité de Défaut')

    fig1.update_layout(**custom_layout)

    return(fig1)

def compare_pop():
    default_proba_avant = model_classique.default_proba_before
    default_proba_apres = model_classique.default_proba

    classes = default_proba_avant['Classe']
    prop_avant = default_proba_avant['Taux_Individus']
    prop_apres = default_proba_apres['Taux_Individus']

    diff_prop = [p2 - p1 for p1, p2 in zip(prop_avant, prop_apres)]

    trace_avant = go.Bar(x=classes, y=prop_avant, name='Avant')
    trace_apres = go.Bar(x=classes, y=prop_apres, name='Après')
    trace_diff = go.Bar(x=classes, y=diff_prop, name='Différence')

    fig = go.Figure(data=[trace_avant, trace_apres, trace_diff])

    fig.update_layout(
        xaxis=dict(title='Classe'),
        yaxis=dict(title='Taux de Population'),
        barmode='group',
        margin = dict(l=0, r=0, t=10, b=0)
    )

    fig.update_layout(**custom_layout)
    return(fig)
