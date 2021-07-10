
def save_app_state_with_dialog(app_name, data):
    pass
    # logger.debug("save_app_state_with_dialog {}".format(app_name))

    # old_level, _, old_xp = calculate_kano_level()
    # old_badges = calculate_badges()

    # save_app_state(app_name, data)

    # new_level, _, new_xp = calculate_kano_level()
    # new_badges = calculate_badges()

    # TODO: This function needs a bit of refactoring in the future
    # # The notifications no longer need to be concatenated to a string

    # # new level
    # new_level_str = ''
    # if old_level != new_level:
    #     new_level_str = 'level:{}'.format(new_level)

    # new items
    # new_items_str = ''
    # badge_changes = compare_badges_dict(old_badges, new_badges)
    # if badge_changes:
    #     for category, subcats in badge_changes.items():
    #         for subcat, items in subcats.items():
    #             for item, rules in items.items():
    #                 new_items_str += ' {}:{}:{}'.format(category, subcat, item)

    # # Check if XP has changed, if so play sound in the backgrond
    # if old_xp != new_xp:
    #     sound_cmd = 'aplay /usr/share/kano-media/sounds/kano_xp.wav > /dev/null 2>&1 &'
    #     run_bg(sound_cmd)

    # if not new_level_str and not new_items_str:
    #     return

    # if is_gui():
    #     # Open the fifo in append mode, as if it is not
    #     # present, notifications are queued in a flat file
    #     notifications = (new_level_str + ' ' + new_items_str).split(' ')

    #     # Write  to both the dashboard and the desktop widget
    #     f1 = os.path.join(os.path.expanduser('~'), '.kano-notifications.fifo')
    #     f2 = os.path.join(os.path.expanduser('~'), '.kano-notifications-desktop.fifo')
    #     write_notifications(f1, notifications)
    #     write_notifications(f2, notifications)

    # cmd = '{bin_dir}/kano-sync --sync -s'.format(bin_dir=bin_dir)
    # run_bg(cmd)


def save_app_state_variable_with_dialog(app_name, variable, value):
    pass
    # logger.debug(
    #     'save_app_state_variable_with_dialog {} {} {}'
    #     .format(app_name, variable, value)
    # )

    # data = load_app_state(app_name)
    # data[variable] = value

    # save_app_state_with_dialog(app_name, data)

