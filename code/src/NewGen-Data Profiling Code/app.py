import gradio as gr
from pdfProcessingWithRAG import process_pdf_and_ask
from csvValidations import validate_csv, plot_anomalies

# -------------------------------------- Gradio UI --------------------------------------

with gr.Blocks() as app:
    gr.Markdown("## 📄 PDF Q&A & CSV Validation")

    with gr.Tab("📖 PDF Q&A"):
        pdf_file = gr.File(label="Upload PDF File")
        question = gr.Textbox(label="Enter Your Question")
        answer = gr.Textbox(label="Response from RAG Model")
        gr.Button("Ask Question").click(
            process_pdf_and_ask, inputs=[pdf_file, question], outputs=[answer]
        )

    with gr.Tab("📊 CSV Validation"):
        csv_file = gr.File(label="Upload CSV File")
        validated_csv = gr.Dataframe(label="Validated CSV Output")
        scatter_plot = gr.Image(label="Anomaly Scatter Plot")
        download_csv = gr.File(label="Download Processed CSV")

        def process_csv(csv_file):
            validated_df, message, csv_path = validate_csv(csv_file)
            if isinstance(validated_df, str):  # If error message is returned
                return validated_df, None
            plot_path = plot_anomalies(validated_df)
            return validated_df, plot_path, csv_path

        gr.Button("Validate CSV").click(
            process_csv, inputs=[csv_file], outputs=[validated_csv, scatter_plot,download_csv]
        )

if __name__ == "__main__":
    app.launch()
