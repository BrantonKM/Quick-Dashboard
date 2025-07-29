def build_query(section=None, start=None, end=None):
    query = "SELECT section, content::text, fetched_at FROM dashboard_logs WHERE 1=1"
    params = []
    if section:
        query += " AND section = %s"
        params.append(section)
    if start:
        query += " AND fetched_at >= %s"
        params.append(start)
    if end:
        query += " AND fetched_at <= %s"
        params.append(end)
    return query + " ORDER BY fetched_at DESC", params
