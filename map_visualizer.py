# map_visualizer.py - Module de visualisation cartographique corrigé
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict
import numpy as np

class MapVisualizer:
    """Visualiseur de cartes génétiques avec affichage optimisé"""
    
    def __init__(self):
        self.map_style = "open-street-map"
        self.default_zoom = 1
        self.marker_size = 12
        self.map_height = 700
    
    def create_origins_map(self, df: pd.DataFrame) -> go.Figure:
        """Crée la carte des origines génétiques avec approche simplifiée"""
        
        # Calculer le centre et le zoom automatiquement
        center_lat = df["Generated_Latitude"].mean()
        center_lon = df["Generated_Longitude"].mean()
        
        # Calculer un zoom approprié
        lat_range = df["Generated_Latitude"].max() - df["Generated_Latitude"].min()
        lon_range = df["Generated_Longitude"].max() - df["Generated_Longitude"].min()
        max_range = max(lat_range, lon_range)
        
        if max_range > 120:
            zoom = 0.5
        elif max_range > 60:
            zoom = 1
        elif max_range > 30:
            zoom = 2
        elif max_range > 15:
            zoom = 3
        else:
            zoom = 4
        
        # Créer la figure manuellement pour éviter les erreurs px
        fig = go.Figure()
        
        # Ajouter une trace par pays pour les couleurs
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FECA57', '#FF9FF3', '#54A0FF', '#5F27CD', '#00D2D3', '#FF9F43', '#2ED573', '#3742FA']
        
        for i, country in enumerate(df['Country_Name'].unique()):
            country_data = df[df['Country_Name'] == country]
            color = colors[i % len(colors)]
            
            fig.add_trace(
                go.Scattermapbox(
                    lat=country_data['Generated_Latitude'],
                    lon=country_data['Generated_Longitude'],
                    mode='markers',
                    marker=dict(
                        size=12,
                        color=color,
                        opacity=0.8
                    ),
                    name=country,
                    text=[f"ID: {row['ID']}<br>Pays: {row['Country_Name']}<br>Confiance: {row['Origin_Confidence']:.3f}" 
                          for _, row in country_data.iterrows()],
                    hovertemplate='<b>%{text}</b><extra></extra>'
                )
            )
        
        # Configuration de la carte
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=center_lat, lon=center_lon),
                zoom=zoom
            ),
            height=self.map_height,
            margin={"r": 10, "t": 60, "l": 10, "b": 10},
            title="🗺️ Distribution géographique des origines génétiques",
            legend=dict(
                yanchor="top", y=0.95,
                xanchor="left", x=0.02,
                bgcolor="rgba(0,0,0,0.8)",
                bordercolor="rgba(255,255,255,0.3)",
                borderwidth=1,
                font=dict(color='white', size=10)
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title_x=0.5
        )
        
        return fig
    
    def create_kinship_map(self, df: pd.DataFrame, relationships: List[Dict]) -> go.Figure:
        """Crée la carte avec les relations familiales"""
        fig = self.create_origins_map(df)
        fig.update_layout(title="🔗 Carte génétique avec relations familiales")
        
        if relationships:
            # Filtrer les relations significatives
            significant_relations = [r for r in relationships if r['Coefficient'] >= 0.05]
            
            # Grouper par type de relation
            relations_by_type = {}
            for rel in significant_relations:
                rel_type = rel['Relation']
                if rel_type not in relations_by_type:
                    relations_by_type[rel_type] = []
                relations_by_type[rel_type].append(rel)
            
            # Ajouter les lignes de relation (limiter pour éviter surcharge)
            for rel_type, relations in relations_by_type.items():
                # Trier par coefficient et prendre les 3 meilleures par type
                relations = sorted(relations, key=lambda x: x['Coefficient'], reverse=True)[:3]
                
                for idx, rel in enumerate(relations):
                    line_width = max(3, min(10, rel['Coefficient'] * 25))
                    opacity = min(0.8, rel['Coefficient'] * 2)
                    
                    fig.add_trace(
                        go.Scattermapbox(
                            mode="lines",
                            lon=[rel['Lon1'], rel['Lon2']],
                            lat=[rel['Lat1'], rel['Lat2']],
                            line=dict(
                                width=line_width, 
                                color=rel['Color']
                            ),
                            opacity=opacity,
                            name=f"{rel_type}" if idx == 0 else "",
                            legendgroup=rel_type,
                            showlegend=(idx == 0),
                            hovertemplate=f"""
                            <b>{rel['ID1']} ↔ {rel['ID2']}</b><br>
                            <b>Relation:</b> {rel_type}<br>
                            <b>Coefficient:</b> {rel['Coefficient']:.4f}<br>
                            <extra></extra>
                            """
                        )
                    )
        
        return fig
    
    def _style_map(self, fig: go.Figure, center_lat: float, center_lon: float, zoom: float):
        """Applique le style optimisé à la carte"""
        fig.update_layout(
            mapbox=dict(
                style=self.map_style,
                center=dict(lat=center_lat, lon=center_lon),
                zoom=zoom,
                # Améliorer les performances en limitant les interactions
                bearing=0,
                pitch=0
            ),
            margin={"r": 10, "t": 60, "l": 10, "b": 10},
            legend=dict(
                yanchor="top", 
                y=0.95, 
                xanchor="left", 
                x=0.02,
                bgcolor="rgba(0,0,0,0.8)", 
                bordercolor="rgba(255,255,255,0.3)",
                borderwidth=1, 
                font=dict(color='white', size=10),
                # Optimiser l'affichage de la légende
                itemsizing="constant",
                traceorder="normal"
            ),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=12),
            title=dict(
                font_size=16,
                x=0.5,  # Centrer le titre
                y=0.95
            ),
            # Améliorer les performances
            dragmode="pan"
        )
        
        # Optimiser les marqueurs
        fig.update_traces(
            selector=dict(mode='markers'),
            marker=dict(
                size=self.marker_size, 
                opacity=0.8,
                line=dict(width=2, color='white')
            )
        )
        
        # Configuration pour éviter les problèmes d'affichage
        fig.update_geos(
            projection_type="natural earth"
        )
    
    def create_statistics_charts(self, df: pd.DataFrame, relationships: List[Dict] = None):
        """Crée des graphiques statistiques optimisés"""
        charts = {}
        
        # Graphique des origines
        if "Country_Name" in df.columns:
            country_counts = df["Country_Name"].value_counts()
            
            # Limiter à 10 pays max pour lisibilité
            if len(country_counts) > 10:
                top_countries = country_counts.head(10)
                others_count = country_counts.tail(-10).sum()
                if others_count > 0:
                    top_countries['Autres'] = others_count
                country_counts = top_countries
            
            charts['origins_pie'] = px.pie(
                values=country_counts.values,
                names=country_counts.index,
                title="Répartition par pays d'origine",
                height=400
            )
            self._style_chart(charts['origins_pie'])
        
        # Graphique des relations si disponible
        if relationships and len(relationships) > 0:
            rel_df = pd.DataFrame(relationships)
            relation_counts = rel_df['Relation'].value_counts()
            
            charts['relations_bar'] = px.bar(
                x=relation_counts.values,
                y=relation_counts.index,
                orientation='h',
                title="Types de relations familiales",
                height=400
            )
            self._style_chart(charts['relations_bar'])
        
        return charts
    
    def _style_chart(self, fig: go.Figure):
        """Style optimisé pour les graphiques"""
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white', size=11),
            title=dict(
                font_size=14,
                x=0.5
            ),
            showlegend=True,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        # Améliorer l'affichage selon le type
        if fig.data[0].type == 'pie':
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percent: %{percent}<extra></extra>'
            )
        elif fig.data[0].type == 'bar':
            fig.update_traces(
                hovertemplate='<b>%{y}</b><br>Count: %{x}<extra></extra>'
            )
            fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.2)')
            fig.update_yaxes(showgrid=False)
    
    def create_world_overview(self, df: pd.DataFrame) -> go.Figure:
        """Crée une vue d'ensemble mondiale optimisée"""
        fig = go.Figure()
        
        # Ajouter les points par pays
        for country in df['Country_Name'].unique():
            country_data = df[df['Country_Name'] == country]
            
            fig.add_trace(
                go.Scattermapbox(
                    lat=country_data['Generated_Latitude'],
                    lon=country_data['Generated_Longitude'],
                    mode='markers',
                    marker=dict(size=12, opacity=0.7),
                    name=country,
                    text=[f"ID: {row['ID']}<br>Pays: {row['Country_Name']}<br>Confiance: {row['Origin_Confidence']:.3f}" 
                          for _, row in country_data.iterrows()],
                    hovertemplate='%{text}<extra></extra>'
                )
            )
        
        # Configuration globale optimisée
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                zoom=1,
                center=dict(lat=20, lon=0)
            ),
            height=600,
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
            title="Vue d'ensemble mondiale des origines",
            title_x=0.5,
            showlegend=True,
            legend=dict(
                yanchor="top",
                y=0.98,
                xanchor="left",
                x=0.02,
                bgcolor="rgba(0,0,0,0.8)",
                font=dict(color='white', size=10)
            )
        )
        
        return fig

    def create_simple_scatter_map(self, df: pd.DataFrame) -> go.Figure:
        """Version simplifiée en cas de problème avec px.scatter_mapbox"""
        fig = go.Figure()
        
        # Créer une trace par pays pour la couleur
        for country in df['Country_Name'].unique():
            country_data = df[df['Country_Name'] == country]
            
            fig.add_trace(
                go.Scattermapbox(
                    lat=country_data['Generated_Latitude'],
                    lon=country_data['Generated_Longitude'],
                    mode='markers',
                    marker=dict(
                        size=10,
                        opacity=0.8
                    ),
                    name=country,
                    hovertemplate='<b>%{text}</b><extra></extra>',
                    text=[f"{row['ID']}<br>{row['Country_Name']}<br>Confiance: {row['Origin_Confidence']:.3f}" 
                          for _, row in country_data.iterrows()]
                )
            )
        
        # Configuration de la carte
        center_lat = df["Generated_Latitude"].mean()
        center_lon = df["Generated_Longitude"].mean()
        
        fig.update_layout(
            mapbox=dict(
                style="open-street-map",
                center=dict(lat=center_lat, lon=center_lon),
                zoom=2
            ),
            height=700,
            margin={"r": 0, "t": 40, "l": 0, "b": 0},
            showlegend=True,
            legend=dict(
                yanchor="top", y=0.98,
                xanchor="left", x=0.02,
                bgcolor="rgba(0,0,0,0.8)",
                font=dict(color='white', size=10)
            )
        )
        
        return fig
