import sys
import json

class DocumentAstParser:
    @staticmethod
    def parse_markdown(text):
        lines = text.splitlines()
        nodes = []
        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                continue
            if trimmed.startswith("#"):
                lvl = len(trimmed) - len(trimmed.lstrip("#"))
                nodes.append({"type": "heading", "level": lvl, "text": trimmed.lstrip("#").strip()})
            elif trimmed.startswith("- ") or trimmed.startswith("* "):
                nodes.append({"type": "list_item", "text": trimmed[2:].strip()})
            elif trimmed.startswith("|") and trimmed.endswith("|"):
                cols = [c.strip() for c in trimmed.strip("|").split("|")]
                nodes.append({"type": "table_row", "columns": cols})
            elif trimmed.startswith("```"):
                nodes.append({"type": "code_fence", "meta": trimmed[3:].strip()})
            else:
                nodes.append({"type": "paragraph", "text": trimmed})
        return {"nodes": nodes, "count": len(nodes)}

    @staticmethod
    def compile_nodes(nodes):
        output = []
        for n in nodes:
            t = n.get("type")
            if t == "heading":
                prefix = "#" * n.get("level", 1)
                output.append(f"{prefix} {n.get('text', '')}")
            elif t == "list_item":
                output.append(f"- {n.get('text', '')}")
            elif t == "paragraph":
                output.append(f"{n.get('text', '')}\n")
            elif t == "code_fence":
                output.append(f"```{n.get('meta', '')}")
            elif t == "table_row":
                cols = n.get("columns", [])
                output.append("| " + " | ".join(cols) + " |")
        return "\n".join(output)

def handle_rpc(request):
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "parse_markdown_ast",
                        "description": "Parse raw markdown into AST nodes.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"markdown": {"type": "string"}},
                            "required": ["markdown"]
                        }
                    },
                    {
                        "name": "compile_ast_markdown",
                        "description": "Compile AST nodes back into canonical markdown.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {"nodes": {"type": "array", "items": {"type": "object"}}},
                            "required": ["nodes"]
                        }
                    }
                ]
            }
        }

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "parse_markdown_ast":
            res = DocumentAstParser.parse_markdown(args.get("markdown", ""))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}
        elif name == "compile_ast_markdown":
            res = DocumentAstParser.compile_nodes(args.get("nodes", []))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": res}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()
