import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WaitTimesVisualizer:
    def __init__(self, wait_times_data: Dict[str, pd.DataFrame]):
        """
        Initialize the visualizer with wait times data.
        
        Args:
            wait_times_data (Dict[str, pd.DataFrame]): Dictionary containing DataFrames for different procedures
        """
        self.wait_times_data = wait_times_data
        self.procedures = list(wait_times_data.keys())
        self.metrics = ['% Meeting Benchmark', '50th Percentile', '90th Percentile', 'Volume']
        
    def prepare_provincial_data(self, procedure: str) -> pd.DataFrame:
        """
        Prepare data for provincial level visualization.
        
        Args:
            procedure (str): The medical procedure to analyze
            
        Returns:
            pd.DataFrame: Processed data for provincial level analysis
        """
        try:
            # Filter for provincial level data only
            df = self.wait_times_data[procedure]
            provincial_data = df[df['Reporting level'] == 'Provincial'].copy()
            
            # Pivot the data for easier plotting
            pivoted_data = pd.pivot_table(
                provincial_data,
                values='Indicator result',
                index=['Province/territory', 'Data year'],
                columns=['Metric'],
                aggfunc='first'
            ).reset_index()
            
            return pivoted_data
            
        except Exception as e:
            logger.error(f"Error preparing provincial data: {str(e)}")
            raise

    def create_comparative_plots(self, procedure: str) -> go.Figure:
        """
        Create comparative plots for different metrics of a procedure.
        
        Args:
            procedure (str): The medical procedure to visualize
            
        Returns:
            go.Figure: Plotly figure object containing the subplots
        """
        try:
            # Prepare the data
            plot_data = self.prepare_provincial_data(procedure)
            
            # Create subplots - one for each metric
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=(
                    '% Meeting Benchmark',
                    '50th Percentile Wait Time (Days)',
                    '90th Percentile Wait Time (Days)',
                    'Volume of Procedures'
                ),
                vertical_spacing=0.15,
                horizontal_spacing=0.1
            )
            
            # Add traces for each province
            for province in plot_data['Province/territory'].unique():
                province_data = plot_data[plot_data['Province/territory'] == province]
                
                # % Meeting Benchmark
                fig.add_trace(
                    go.Scatter(
                        x=province_data['Data year'],
                        y=province_data['% Meeting Benchmark'],
                        name=province,
                        showlegend=True,
                        mode='lines+markers'
                    ),
                    row=1, col=1
                )
                
                # 50th Percentile
                fig.add_trace(
                    go.Scatter(
                        x=province_data['Data year'],
                        y=province_data['50th Percentile'],
                        name=province,
                        showlegend=False,
                        mode='lines+markers'
                    ),
                    row=1, col=2
                )
                
                # 90th Percentile
                fig.add_trace(
                    go.Scatter(
                        x=province_data['Data year'],
                        y=province_data['90th Percentile'],
                        name=province,
                        showlegend=False,
                        mode='lines+markers'
                    ),
                    row=2, col=1
                )
                
                # Volume
                fig.add_trace(
                    go.Scatter(
                        x=province_data['Data year'],
                        y=province_data['Volume'],
                        name=province,
                        showlegend=False,
                        mode='lines+markers'
                    ),
                    row=2, col=2
                )
            
            # Update layout
            fig.update_layout(
                height=800,
                title_text=f"{procedure.replace('_', ' ').title()} - Provincial Comparison",
                title_x=0.5,
                font=dict(size=10),
                template='plotly_white'
            )
            
            # Update axes labels
            fig.update_xaxes(title_text="Year", row=2, col=1)
            fig.update_xaxes(title_text="Year", row=2, col=2)
            
            fig.update_yaxes(title_text="Percentage", row=1, col=1)
            fig.update_yaxes(title_text="Days", row=1, col=2)
            fig.update_yaxes(title_text="Days", row=2, col=1)
            fig.update_yaxes(title_text="Number of Cases", row=2, col=2)
            
            return fig
            
        except Exception as e:
            logger.error(f"Error creating comparative plots: {str(e)}")
            raise

    def get_available_procedures(self) -> List[str]:
        """
        Get list of available procedures for visualization.
        
        Returns:
            List[str]: List of procedure names
        """
        return self.procedures

    def get_available_metrics(self) -> List[str]:
        """
        Get list of available metrics for visualization.
        
        Returns:
            List[str]: List of metric names
        """
        return self.metrics