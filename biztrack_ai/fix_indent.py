import re
import textwrap

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    def dedent_match(m):
        s = m.group(0)
        inner = s[3:-3]
        # Dedent the inner string
        dedented = textwrap.dedent(inner)
        return '"""' + dedented + '"""'
    
    new_content = re.sub(r'"""(.*?)"""', dedent_match, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

fix_file('utils.py')
fix_file('app.py')
print('Fixed!')
