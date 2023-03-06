{#- Generate an extension module header file of doc strings #}

{%- macro cmacro(item) %}
{%-   set name = item['fullname']|replace('_', '') %}
{{-   'DOC_' + name.split('.')[1:]|join('_')|upper }}
{%- endmacro %}

{%- macro join_sigs(item) %}
{%-   set sigs = item['signatures'] %}
{%-   if sigs %}
{{-     sigs|join('\\n') + '\\n' }}
{%-   else %}
{{-     '' }}
{%-   endif %}
{%- endmacro %}

{#- -#}


/* Auto generated file: with makeref.py .  Docs go in docs/reST/ref/ . */
{% for item in hdr_items -%}
#define {{ cmacro(item) }} "{{ join_sigs(item) }}{{ item['summary'] }}"
{% endfor %}
