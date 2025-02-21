import streamlit as st
from code.extract_data import DataExtractor
from code.visualise_data import WaitTimesVisualizer

def main():
    st.title("Healthcare Wait Times Analysis")
    
    try:
        # Initialize data extractor
        extractor = DataExtractor("assets")
        wait_times_data = extractor.extract_wait_times()
        
        # Initialize visualizer
        visualizer = WaitTimesVisualizer(wait_times_data)
        
        # Create sidebar for procedure selection
        st.sidebar.header("Filters")
        selected_procedure = st.sidebar.selectbox(
            "Select Procedure",
            visualizer.get_available_procedures(),
            format_func=lambda x: x.replace('_', ' ').title()
        )
        
        # Create and display the comparative plots
        st.header(f"Comparative Analysis - {selected_procedure.replace('_', ' ').title()}")
        fig = visualizer.create_comparative_plots(selected_procedure)
        st.plotly_chart(fig, use_container_width=True)
        
        # Add description
        st.markdown("""
        ### Plot Description
        This visualization shows four key metrics for the selected procedure:
        1. **% Meeting Benchmark**: Percentage of procedures meeting the recommended wait time benchmark
        2. **50th Percentile**: Median wait time in days
        3. **90th Percentile**: 90th percentile of wait times in days
        4. **Volume**: Number of procedures performed
        
        Each line represents a different province/territory, allowing for easy comparison across regions.
        """)
        
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()