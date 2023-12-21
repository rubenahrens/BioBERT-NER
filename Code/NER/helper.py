from IPython.display import display, HTML

def write_tex_table(all_metrics, filename):
    with open(filename, 'w') as f:
        f.write("\\begin{table}[h]\n")
        f.write("\\centering\n")
        f.write("\\begin{tabular}{lrrrr}\n")
        f.write("\\toprule\n")
        f.write(" & \\textbf{Precision} & \\textbf{Recall} & \\textbf{F1} & \\textbf{Number} \\\\\n")
        f.write("\\midrule\n")
        for key, value in all_metrics.items():
            if "overall" not in key:
                f.write(f"{key.title()} & {value['precision']:.2f} & {value['recall']:.2f} & {value['f1']:.2f} & {value['number']} \\\\\n")
        try:
            f.write("\\midrule\n")
            f.write(" & \\textbf{Overall precision} & \\textbf{Overall recall} & \\textbf{Overall F1} & \\textbf{Overall accuracy} \\\\\n")
            f.write("\\midrule\n")
            f.write(f" & {all_metrics['overall_precision']:.2f} & {all_metrics['overall_recall']:.2f} & {all_metrics['overall_f1']:.2f} & {all_metrics['overall_accuracy']:.2f} \\\\\n")
        except:
            pass
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n")
    
def print_fancy_table(all_metrics):
    # display fancy table in ipython widget
    html = "<table>"
    html += "<tr><th></th><th>Precision</th><th>Recall</th><th>F1</th><th>Number</th></tr>"
    for key, value in all_metrics.items():
        if "overall" not in key:
            html += f"<tr><td>{key.title()}</td><td>{value['precision']:.2f}</td><td>{value['recall']:.2f}</td><td>{value['f1']:.2f}</td><td>{value['number']}</td></tr>"
    html += "<tr><th></th><th>Overall precision</th><th>Overall recall</th><th>Overall F1</th><th>Overall accuracy</th></tr>"
    html += f"<tr><td></td><td>{all_metrics['overall_precision']:.2f}</td><td>{all_metrics['overall_recall']:.2f}</td><td>{all_metrics['overall_f1']:.2f}</td><td>{all_metrics['overall_accuracy']:.2f}</td></tr>"
    html += "</table>"
    display(HTML(html))
    