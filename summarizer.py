def summarize_transformation(tf):
    lines = [f"### 🔄 Transformation: {tf['name']} ({tf['type']})"]
    if tf['sql_override']:
        lines.append("**SQL Override:**")
        lines.append(f"```sql\n{tf['sql_override']}\n```")
    
    lines.append("**Fields:**")
    for f in tf['fields']:
        expression = f['expression']
        if expression:
            logic_summary = f"Expression: `{expression}`"
        else:
            logic_summary = "No logic"
        lines.append(f"- `{f['name']}` ({f['datatype']}, {f['porttype']}) → {logic_summary}")
    return "\n".join(lines)
