gfx r n REGION1
gfx r e REGION1
gfx r d REGION1
gfx modify g_element DATA general clear circle_discretization 6 default_coordinate coordinates element_discretization "4*4*4" native_discretization none;
gfx modify g_element DATA lines select_on material default selected_material default_selected;
gfx modify g_element DATA data_points glyph sphere general size "0.1*0.1*0.1" centre 0,0,0 font default select_on material default selected_material default_selected;
gfx cre win
