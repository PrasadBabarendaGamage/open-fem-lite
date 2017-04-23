fem def para;r;para
fem def coor;r;REGION1
fem def base;r;REGION1
fem def node;r;REGION1
fem def elem;r;REGION1
fem export node;REGION1 offset 1000 as REGION1
fem export elem;REGION1 offset_elem 1000 as REGION1
q
