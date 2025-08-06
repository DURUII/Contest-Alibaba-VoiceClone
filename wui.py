import gradio as gr
import pandas as pd
import os

# 读取任务csv
csv_path = 'aigc_speech_generation_tasks/aigc_speech_generation_tasks.csv'
df = pd.read_csv(csv_path)

# simple-baseline和strong-baseline的结果路径
simple_result_dir = 'simple-baseline/result'
strong_result_dir = 'strong-baseline/result'
reference_dir = 'aigc_speech_generation_tasks'

def get_audio_path(directory, filename):
    path = os.path.join(directory, filename)
    return path if os.path.exists(path) else None

def build_examples(start_index=0):
    examples = []
    # Generate examples starting from the selected index
    for idx, row in df.iloc[start_index:start_index+10].iterrows():
        utt = row['utt']
        text = row['text']
        ref_audio = get_audio_path(reference_dir, row['reference_speech'])
        simple_audio = get_audio_path(simple_result_dir, f"{utt}.wav")
        strong_audio = get_audio_path(strong_result_dir, f"{utt}.wav")
        examples.append({
            'utt': utt,
            'text': text,
            'reference': ref_audio,
            'simple': simple_audio,
            'strong': strong_audio
        })
    return examples

def update_examples(start_index):
    return build_examples(start_index)

# Options for dropdown
start_options = [i for i in range(0, len(df), 10)]

# Text content moved to variables
title_text = "# 2025全球AI攻防挑战赛：泛终端智能语音交互认证（语音生成赛）"
description_text = ""
dropdown_label = "选择起始 utt-id 项"
no_audio_text = "无"
reference_label = "参考音频"
simple_baseline_label = "simple-baseline"
strong_baseline_label = "strong-baseline"

with gr.Blocks() as demo:
    gr.Markdown(title_text)
    
    # Dropdown for selecting the starting index
    start_index_dropdown = gr.Dropdown(label=dropdown_label, choices=start_options, value=0)

    # Create a dynamic display for examples
    output = gr.Column()

    # Function to update the display based on selected start index
    start_index_dropdown.change(fn=update_examples, inputs=start_index_dropdown, outputs=output)
    
    # Initially load examples for the first page
    examples = build_examples(0)
    for ex in examples:
        with output:
            # First Row: utt and text
            with gr.Row(equal_height=True):
                gr.Textbox(value=ex['utt'], label="utt", interactive=False, show_label=True, scale=1)
                gr.Textbox(value=ex['text'], label="文本", interactive=False, show_label=True, scale=3)
            
            # Second Row: Audio components (reference, simple-baseline, strong-baseline)
            with gr.Row(equal_height=True):
                with gr.Column(scale=1):
                    if ex['reference']:
                        gr.Audio(ex['reference'], label=reference_label, elem_id="reference_audio")
                    else:
                        gr.Textbox(no_audio_text, label=reference_label, interactive=False)
                
                with gr.Column(scale=1):
                    if ex['simple']:
                        gr.Audio(ex['simple'], label=simple_baseline_label, elem_id="simple_audio")
                    else:
                        gr.Textbox(no_audio_text, label=simple_baseline_label, interactive=False)
                
                with gr.Column(scale=1):
                    if ex['strong']:
                        gr.Audio(ex['strong'], label=strong_baseline_label, elem_id="strong_audio")
                    else:
                        gr.Textbox(no_audio_text, label=strong_baseline_label, interactive=False)
                
demo.launch()
