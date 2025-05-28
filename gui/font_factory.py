import os
from PySide6.QtGui import QFontDatabase, QFont


def font_factory(core=None):
    if not core:
        raise ValueError("Core object is required.")

    wr = core.widget_registry

    font_folder = 'fonts'
    font_id = QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), font_folder, 'Aquire-BW0ox.otf'))
    if font_id == -1:
        raise Exception("Failed to load the custom font.")
    else:
        core.project_font = QFontDatabase.applicationFontFamilies(font_id)[0]

    font_objects = [(wr['misc']['title_right_info'], 12),
                    #(ui.last_udpate_label, 12),
                    #(wr['general']['btn_toggle'], 8),
                    (wr['general']['btn_home'], 8),
                    (wr['general']['btn_bwd'], 8),
                    (wr['general']['btn_box_spread'], 16),
                    (wr['general']['label_header'], 18),

                    (wr['beta_weighted_deltas']['list_selection'], 18),
                    (wr['beta_weighted_deltas']['table_greeks'], 12),

                    (wr['box_spread']['btn_type'], 14),
                    (wr['box_spread']['label_currency'], 14),
                    (wr['box_spread']['comboBox_currency'], 14),
                    (wr['box_spread']['comboBox_index'], 14),
                    (wr['box_spread']['label_index'], 14),
                    (wr['box_spread']['label_type'], 14),
                    (wr['box_spread']['comboBox_type'], 14),
                    (wr['box_spread']['label_expiry'], 14),
                    (wr['box_spread']['comboBox_expiry'], 14),
                    (wr['box_spread']['label_higher_rate'], 10),
                    (wr['box_spread']['label_lower_rate'], 10),
                    (wr['box_spread']['label_benchmark_rate'], 10),
                    (wr['box_spread']['label_selected_rate'], 12),
                    (wr['box_spread']['label_upper_strike'], 14),
                    (wr['box_spread']['comboBox_upper_strike'], 14),
                    (wr['box_spread']['label_lower_strike'], 14),
                    (wr['box_spread']['comboBox_lower_strike'], 14),
                    (wr['box_spread']['label_spread'], 14),
                    (wr['box_spread']['label_amount'], 14),
                    (wr['box_spread']['line_amount'], 14),
                    (wr['box_spread']['label_selected_rate'], 14),
                    (wr['box_spread']['label_underlying_price'], 14),


                    (wr['box_spread']['label_multiplier'], 14),
                    (wr['box_spread']['label_initial'], 14),
                    (wr['box_spread']['label_nominal'], 14),

    ]

    for obj, size in font_objects:
        font = QFont(core.project_font, size)
        obj.setFont(font)