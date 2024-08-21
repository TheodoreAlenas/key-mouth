
def events_to_socket_model(events, first_moment_idx, first_diff_idx):
    mi = first_moment_idx
    di = first_diff_idx
    ans = []
    for e in events:
        t = e.event_type
        ans.append({
            'momentIdx': mi,
            'diffIdx': di,
            'connId': e.conn_id,
            'type': t,
            'body': e.body
        })
        if t == 'endOfMoment':
            di = 0
            mi += 1
        else:
            di += 1
    return ans
