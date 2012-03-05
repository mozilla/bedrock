int x_step;
int x_width;
int bar_height;
int width = 128;
int height = 128;

void setup() {
    size(128, 128);
    noLoop();
}

void draw() {
    background(0, 0, 0, 0);
    noStroke();
    fill(225, 230, 233, 255);

    if ( bd.beat_counter % 4 == 0 ) {
        rect(2, 2, 60, 60);
    } else if ( bd.beat_counter % 4 == 1 ) {
        rect(2, 66, 60, 60);
    } else if ( bd.beat_counter % 4 == 2 ) {
        rect(66, 66, 60, 60);
    } else if ( bd.beat_counter % 4 == 3 ) {
        rect(66, 2, 60, 60);
    }

    strokeWeight(0.0);

    if (vu.vu_levels.length) {
        int x_step = (width/(bd.config.BD_DETECTION_RANGES/4));
        int x_width = (width/(bd.config.BD_DETECTION_RANGES/4))-2;

        fill(108, 207, 228, 255);
        for (int i = 0; i < bd.config.BD_DETECTION_RANGES/4; i++) {
            int v_i = i;

            int sz;
            sz = 64*vu.vu_levels[v_i];
            if (sz>64) sz = 64;

            rect(i*x_step,128-sz,2,sz);
        }
    }

    strokeWeight(3);
    stroke(108, 207, 228, 255);

    for ( int i = 0; i < 128; i++) {
        float mi = Math.abs(signal[4*i]);
        line(i, 32 - signal[4*i] * 32, i + 1, 32 - signal[4*(i+1)] * 32)
    }
}

