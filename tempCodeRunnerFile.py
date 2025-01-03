# Send turn-off command asynchronously in a separate thread
turn_off_thread = threading.Thread(target=send_turn_off_command)
turn_off_thread.start()