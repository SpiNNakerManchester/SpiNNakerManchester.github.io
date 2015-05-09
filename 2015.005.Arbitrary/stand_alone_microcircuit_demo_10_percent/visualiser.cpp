#include <iostream>
#include <GL/glut.h>
#include <GL/freeglut.h>
#include <math.h>
#include <stdio.h>
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <sys/time.h>
#ifndef WIN32
#include <netinet/in.h>
#include <netdb.h>
#include <arpa/inet.h>
#else
#define _WIN32_WINNT 0x501
#include <ws2tcpip.h>
#include <winsock2.h>
#define bzero(b,len) (memset((b), '\0', (len)), (void) 0)
#define bcopy(b1,b2,len) (memmove((b2), (b1), (len)), (void) 0)
typedef unsigned int uint;
typedef unsigned short ushort;
#endif
#include <signal.h>
#include <errno.h>
#include <pthread.h>
#include <unistd.h>  // included for Fedora 17 Fedora17  28th September 2012 - CP
#include <map>
#include <deque>
using namespace std;

#define TRUE 1
#define FALSE 0
#ifdef WIN32

static void
nanosleep (const struct timespec *requested_delay, struct timespec *remain)
{
    if (requested_delay->tv_sec > 0)
    /* At least one second. Millisecond resolution is sufficient. */
    Sleep (requested_delay->tv_sec * 1000 + requested_delay->tv_nsec / 1000000);
    else
    {
        /* Use Sleep for the largest part, and busy-loop for the rest. */
        static double frequency;
        if (frequency == 0)
        {
            LARGE_INTEGER freq;
            if (!QueryPerformanceFrequency (&freq))
            {
                /* Cannot use QueryPerformanceCounter. */
                Sleep (requested_delay->tv_nsec / 1000000);
                return;
            }
            frequency = (double) freq.QuadPart / 1000000000.0;
        }
        long long expected_counter_difference = requested_delay->tv_nsec *
        frequency;
        int sleep_part = (int) requested_delay->tv_nsec / 1000000 - 10;
        LARGE_INTEGER before;
        QueryPerformanceCounter (&before);
        long long expected_counter = before.QuadPart +
        expected_counter_difference;
        if (sleep_part > 0)
        Sleep (sleep_part);
        for (;;)
        {
            LARGE_INTEGER after;
            QueryPerformanceCounter (&after);
            if (after.QuadPart >= expected_counter)
            break;
        }
    }
}
int
inet_aton(const char *cp_arg, struct in_addr *addr)
{
    register const u_char *cp = (const u_char *) cp_arg;
    register u_long val;
    register int base;
#ifdef WIN32
    register ULONG_PTR n;
#else
    register unsigned long n;
#endif
    register u_char c;
    u_int parts[4];
    register u_int *pp = parts;

    for (;;) {
        /*
         * Collect number up to ``.''.
         * Values are specified as for C:
         * 0x=hex, 0=octal, other=decimal.
         */
        val = 0; base = 10;
        if (*cp == '0') {
            if (*++cp == 'x' || *cp == 'X')
            base = 16, cp++;
            else
            base = 8;
        }
        while ((c = *cp) != '\0') {
            if (isascii(c) && isdigit(c)) {
                val = (val * base) + (c - '0');
                cp++;
                continue;
            }
            if (base == 16 && isascii(c) && isxdigit(c)) {
                val = (val << 4) +
                (c + 10 - (islower(c) ? 'a' : 'A'));
                cp++;
                continue;
            }
            break;
        }
        if (*cp == '.') {
            /*
             * Internet format:
             *  a.b.c.d
             *  a.b.c   (with c treated as 16-bits)
             *  a.b (with b treated as 24 bits)
             */
            if (pp >= parts + 3 || val > 0xff)
            return (0);
            *pp++ = val, cp++;
        } else
        break;
    }
    /*
     * Check for trailing characters.
     */
    if (*cp && (!isascii(*cp) || !isspace(*cp)))
    return (0);
    /*
     * Concoct the address according to
     * the number of parts specified.
     */
    n = pp - parts + 1;
    switch (n) {

        case 1: /* a -- 32 bits */
        break;

        case 2: /* a.b -- 8.24 bits */
        if (val > 0xffffff)
        return (0);
        val |= parts[0] << 24;
        break;

        case 3: /* a.b.c -- 8.8.16 bits */
        if (val > 0xffff)
        return (0);
        val |= (parts[0] << 24) | (parts[1] << 16);
        break;

        case 4: /* a.b.c.d -- 8.8.8.8 bits */
        if (val > 0xff)
        return (0);
        val |= (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8);
        break;
    }
    if (addr)
    addr->s_addr = htonl(val);
    return (1);
}
#endif

#define MAXBLOCKSIZE        364
struct spinnpacket {
    unsigned short version;
    unsigned int cmd_rc;
    unsigned int arg1;
    unsigned int arg2;
    unsigned int arg3;
    unsigned int data[MAXBLOCKSIZE];
};
// a structure that holds SpiNNaker packet data (inside UDP segment)

struct sdp_msg        // SDP message (<=292 bytes)
{
    unsigned char ip_time_out;
    unsigned char pad;
    // sdp_hdr_t
    unsigned char flags;        // SDP flag byte
    unsigned char tag;            // SDP IPtag
    unsigned char dest_port;        // SDP destination port
    unsigned char srce_port;        // SDP source port
    unsigned short dest_addr;        // SDP destination address
    unsigned short srce_addr;        // SDP source address
    // cmd_hdr_t (optional, but tends to be there!)
    unsigned short cmd_rc;        // Command/Return Code
    unsigned short seq;            // seq (new per ST email 27th Oct 2011)
    unsigned int arg1;            // Arg 1
    unsigned int arg2;            // Arg 2
    unsigned int arg3;            // Arg 3
    // user data (optional)
    uint32_t data[MAXBLOCKSIZE];    // User data (256 bytes)
};

int sockfd_input;

// setup socket for SDP frame receiving on port SDPPORT defined about (usually 17894)
int init_sdp_listening(int sdp_port) {
    char portno_input[6];
    snprintf(portno_input, 6, "%d", sdp_port);

    struct addrinfo hints_input;
    bzero(&hints_input, sizeof(hints_input));
    hints_input.ai_family = AF_INET; // set to AF_INET to force IPv4
    hints_input.ai_socktype = SOCK_DGRAM; // type UDP (socket datagram)
    hints_input.ai_flags = AI_PASSIVE; // use my IP

    int rv_input;
    struct addrinfo *servinfo_input;
    if ((rv_input = getaddrinfo(NULL, portno_input, &hints_input,
            &servinfo_input)) != 0) {
        fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(rv_input));
        exit(1);
    }

    // loop through all the results and bind to the first we can
    struct addrinfo *p_input;
    for (p_input = servinfo_input; p_input != NULL; p_input =
            p_input->ai_next) {
        if ((sockfd_input = socket(p_input->ai_family, p_input->ai_socktype,
                p_input->ai_protocol)) == -1) {
            printf("SDP SpiNNaker listener: socket");
            perror("SDP SpiNNaker listener: socket");
            continue;
        }

        if (bind(sockfd_input, p_input->ai_addr, p_input->ai_addrlen) == -1) {
            close(sockfd_input);
            printf("SDP SpiNNaker listener: bind");
            perror("SDP SpiNNaker listener: bind");
            continue;
        }

        break;
    }

    if (p_input == NULL) {
        fprintf(stderr, "SDP listener: failed to bind socket\n");
        printf("SDP listener: failed to bind socket\n");
        exit(-1);
    }

    freeaddrinfo(servinfo_input);

    //printf ("SDP UDP listener setup complete!\n");      // here ends the UDP listener setup witchcraft
}

void *get_in_addr(struct sockaddr *sa) {
    if (sa->sa_family == AF_INET) {
        return &(((struct sockaddr_in*) sa)->sin_addr);
    }

    return &(((struct sockaddr_in6*) sa)->sin6_addr);
}

struct colour {
    float r;
    float g;
    float b;
};

int plotTime = 1000;
float timeStep = 0.1;
int plotNeurons = 8000;
int windowWidth = 800;
int windowHeight = 600;
int windowBorder = 110;
std::map<int, char*> y_axis_labels;
std::map<int, int> key_to_neuronid_map;
std::map<int, struct colour> neuron_id_to_colour_map;
std::deque<std::pair<int, int> > points_to_draw;
bool do_update = FALSE;
pthread_mutex_t spike_mutex;

void* input_thread_SDP(void *ptr) {

    struct sockaddr_in si_other; // for incoming frames
    socklen_t addr_len_input = sizeof(struct sockaddr_in);
    char sdp_header_len = 26;
    unsigned char buffer_input[1515];

    fprintf(stderr, "Listening...\n");

    while (1) {                             // for ever ever, ever ever.

        int numbytes_input = recvfrom(sockfd_input, (char *) buffer_input,
                sizeof(buffer_input), 0, (sockaddr*) &si_other,
                (socklen_t*) &addr_len_input);
        if (numbytes_input == -1) {
            fprintf(stderr, "Packet not received, exiting\n");
            exit(-1); // will only get here if there's an error getting the input frame off the Ethernet
        }
        if (numbytes_input < 18) {
            fprintf(stderr, "Error - packet too short\n");
            continue;
        }

        uint32_t time = buffer_input[17] << 24 | buffer_input[16] << 16
                | buffer_input[15] << 8 | buffer_input[14];

        pthread_mutex_lock(&spike_mutex);
        for (int i = sdp_header_len; i < numbytes_input; i += 4) { // for all extra data (assuming regular array of paired words, word1=key, word2=data)
            uint key = buffer_input[i + 3] << 24 | buffer_input[i + 2] << 16
                    | buffer_input[i + 1] << 8 | buffer_input[i];
            if (key_to_neuronid_map.find(key) == key_to_neuronid_map.end()) {
                fprintf(stderr, "Key %d not recognised!\n", key);
            } else {
                int neurid = key_to_neuronid_map[key];
                points_to_draw.push_back(make_pair(time, neurid));
            }
        }
        do_update = TRUE;
        pthread_mutex_unlock(&spike_mutex);
    }
}

//-------------------------------------------------------------------------
//  Draws a string at the specified coordinates.
//-------------------------------------------------------------------------
void printgl(float x, float y, void *font_style, char* format, ...) {
    va_list arg_list;
    char str[256];
    int i;

    // font options:  GLUT_BITMAP_8_BY_13 GLUT_BITMAP_9_BY_15 GLUT_BITMAP_TIMES_ROMAN_10 GLUT_BITMAP_HELVETICA_10 GLUT_BITMAP_HELVETICA_12 GLUT_BITMAP_HELVETICA_18 GLUT_BITMAP_TIMES_ROMAN_24

    va_start(arg_list, format);
    vsprintf(str, format, arg_list);
    va_end(arg_list);

    glRasterPos2f(x, y);

    for (i = 0; str[i] != '\0'; i++) {
        glutBitmapCharacter(font_style, str[i]);
    }
}

void printglstroke(float x, float y, float size, float rotate, char* format,
        ...) {
    va_list arg_list;
    char str[256];
    int i;
    GLvoid *font_style = GLUT_STROKE_ROMAN;

    va_start(arg_list, format);
    vsprintf(str, format, arg_list);
    va_end(arg_list);

    glPushMatrix();
    glEnable (GL_BLEND);   // antialias the font
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glEnable (GL_LINE_SMOOTH);
    glLineWidth(1.5);   // end setup for antialiasing
    glTranslatef(x, y, 0);
    glScalef(size, size, size);
    glRotatef(rotate, 0.0, 0.0, 1.0);
    for (i = 0; str[i] != '\0'; i++) {
        glutStrokeCharacter(GLUT_STROKE_ROMAN, str[i]);
    }
    glDisable(GL_LINE_SMOOTH);
    glDisable(GL_BLEND);
    glPopMatrix();
}

int window = 0;

void display(void) {
    pthread_mutex_lock(&spike_mutex);
    glPointSize(1.0);
    glutSetWindow(window);

    float x_spacing = (float) (windowWidth - (2 * windowBorder))
            / ((float) plotTime / timeStep);
    float y_spacing = (float) (windowHeight - (2 * windowBorder))
            / (float) plotNeurons;

    glClearColor(1.0, 1.0, 1.0, 1.0);
    glClear (GL_COLOR_BUFFER_BIT);
    glColor4f(0.0, 0.0, 0.0, 1.0);                      // Black Text for Labels

    char title[] = "Raster Plot";
    printgl((windowWidth / 2) - 75, windowHeight - 50,
            GLUT_BITMAP_TIMES_ROMAN_24, title);

    char x_axis[] = "Simulation Time (ms)";
    printglstroke((windowWidth / 2) - 100, 20, 0.12, 0, x_axis);
    char label_0[] = "0";
    printglstroke(windowBorder - 15, windowBorder - 20, 0.10, 0, label_0);
    char label_max[] = "%d";
    printglstroke(windowWidth - windowBorder - 20, windowBorder - 20, 0.10, 0,
            label_max, plotTime);

    for (std::map<int, char*>::iterator iter = y_axis_labels.begin();
            iter != y_axis_labels.end(); ++iter) {
        float y_value = ((iter->first * y_spacing) + windowBorder) - 10;
        char y_label[] = "%s";
        printglstroke(60, y_value, 0.10, 0, y_label, iter->second);
    }

    glColor4f(0.0, 0.0, 0.0, 1.0);
    glLineWidth(1.0);
    glBegin (GL_LINES);
    glVertex2f(windowWidth - windowBorder, windowBorder); // rhs
    glVertex2f(windowBorder - 10, windowBorder); // inside
    glEnd();
    glBegin(GL_LINES);
    glVertex2f(windowBorder - 10, windowBorder);
    glVertex2f(windowBorder - 10, windowHeight - windowBorder);
    glEnd();

    glPointSize(2.0);
    glBegin(GL_POINTS);
    for (std::deque<std::pair<int, int> >::iterator iter =
            points_to_draw.begin(); iter != points_to_draw.end(); ++iter) {
        struct colour colour = neuron_id_to_colour_map[iter->second];
        if (neuron_id_to_colour_map.find(iter->second)
                == neuron_id_to_colour_map.end()) {
            fprintf(stderr, "Missing colour for neuron %d\n", iter->second);
            continue;
        }

        glColor4f(colour.r, colour.g, colour.b, 1.0);
        float x_value = (iter->first * x_spacing) + windowBorder;
        float y_value = (iter->second * y_spacing) + windowBorder;

        glVertex2f(x_value, y_value);
    }
    do_update = FALSE;
    pthread_mutex_unlock(&spike_mutex);
    glEnd();

    glutSwapBuffers();
}

void reshape(int width, int height) {
    if (glutGetWindow() == window) {
        fprintf(stderr, "Reshape to %d, %d\n", width, height);
        windowWidth = width;
        windowHeight = height;

        //printf("Wid: %d, Hei: %d.\n",width,height);
        glViewport(0, 0, (GLsizei) width, (GLsizei) height); // viewport dimensions
        glMatrixMode (GL_PROJECTION);
        glLoadIdentity();
        // an orthographic projection. Should probably look into OpenGL perspective projections for 3D if that's your thing
        glOrtho(0.0, width, 0.0, height, -50.0, 50.0);
        glMatrixMode (GL_MODELVIEW);
        glLoadIdentity();
    }

}

void safelyshut(void) {
    exit(0);                // kill program dead
}

void idleFunction() {
    if (do_update) {
        display();
    }
}

int main(int argc, char **argv) {
#ifdef WIN32
    WSADATA wsaData; // if this doesn't work
    //WSAData wsaData; // then try this instead

    if (WSAStartup(MAKEWORD(1, 1), &wsaData) != 0) {
        fprintf(stderr, "WSAStartup failed.\n");
        exit(1);
    }
#endif

    if (pthread_mutex_init(&spike_mutex, NULL) == -1) {
        fprintf(stderr, "Error initializing mutex!\n");
        exit(-1);
    }

    fprintf(stderr, "Reading keys\n");
    FILE *key_fp = fopen("keys.map", "r");
    char line[80];
    plotNeurons = 0;
    while (fgets(line, 80, key_fp) != NULL) {
        int key;
        int nid;
        sscanf(line, "%d\t%d", &key, &nid);
        key_to_neuronid_map[key] = nid;
        if ((nid + 1) > plotNeurons) {
            plotNeurons = nid + 1;
        }
    }
    fclose(key_fp);

    fprintf(stderr, "Reading colours\n");
    FILE *colour_fp = fopen("colours.map", "r");
    while (fgets(line, 80, colour_fp) != NULL) {
        int nid;
        int r;
        int g;
        int b;
        struct colour colour;
        sscanf(line, "%d\t%d\t%d\t%d", &nid, &r, &g, &b);
        colour.r = (float) r / 255.0;
        colour.g = (float) g / 255.0;
        colour.b = (float) b / 255.0;
        neuron_id_to_colour_map[nid] = colour;
    }
    fclose(colour_fp);

    fprintf(stderr, "Reading labels\n");
    FILE *label_fp = fopen("labels.map", "r");
    while (fgets(line, 80, label_fp) != NULL) {
        int nid;
        char *label = (char *) malloc(80);
        sscanf(line, "%d\t%s\n", &nid, label);
        y_axis_labels[nid] = label;
    }
    fclose(label_fp);

    fprintf(stderr, "Starting\n");
    pthread_t p2; // this sets up the thread that can come back to here from type
    init_sdp_listening(17895); //initialization of the port for receiving SDP frames
    pthread_create(&p2, NULL, input_thread_SDP, NULL); // away the SDP network receiver goes

    glutInit(&argc, argv); /* Initialise OpenGL */

    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB); /* Set the display mode */
    glutInitWindowSize(windowWidth, windowHeight); /* Set the window size */
    glutInitWindowPosition(0, 100); /* Set the window position */
    window = glutCreateWindow("Raster Plot"); /* Create the window */
    glClearColor(0.0, 0.0, 0.0, 1.0);
    glColor3f(1.0, 1.0, 1.0);
    glShadeModel (GL_SMOOTH);
    glutDisplayFunc(display); /* Register the "display" function */
    glutReshapeFunc(reshape); /* Register the "reshape" function */
    glutIdleFunc(idleFunction); /* Register the idle function */
    glutCloseFunc(safelyshut); // register what to do when the use kills the window via the frame object
    glutMainLoop(); /* Enter the main OpenGL loop */

    return 0;
}
