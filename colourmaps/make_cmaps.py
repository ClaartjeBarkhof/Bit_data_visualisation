import matplotlib.colors as mcolors
import pickle

color_dict = {'blue':'#8caadc', 
              'pink':'#fcb1ca', 
              'orange':'#efb116', 
              'dark_blue':'#000563',
              'green':'#005f32',
              'red':'#c51914', 
              'sand':'#cec3bc'}

def hex_to_RGB(hex):
    ''' "#FFFFFF" -> [255,255,255] '''
    # Pass 16 to the integer function for change of base
    return [int(hex[i:i+2], 16) for i in range(1,6,2)]


def RGB_to_hex(RGB):
    ''' [255,255,255] -> "#FFFFFF" '''
    # Components need to be integers for hex to make sense
    RGB = [int(x) for x in RGB]
    return "#"+"".join(["0{0:x}".format(v) if v < 16 else
            "{0:x}".format(v) for v in RGB])

def color_dict_fn(gradient):
    ''' Takes in a list of RGB sub-lists and returns dictionary of
    colors in RGB and hex form for use in a graphing function
    defined later on '''
    return {"hex":[RGB_to_hex(RGB) for RGB in gradient],
             "r":[RGB[0] for RGB in gradient],
             "g":[RGB[1] for RGB in gradient],
             "b":[RGB[2] for RGB in gradient]}


def linear_gradient(start_hex, finish_hex="#FFFFFF", n=10):
    ''' returns a gradient list of (n) colors between
    two hex colors. start_hex and finish_hex
    should be the full six-digit color string,
    inlcuding the number sign ("#FFFFFF") '''
    # Starting and ending colors in RGB form
    s = hex_to_RGB(start_hex)
    f = hex_to_RGB(finish_hex)
    # Initilize a list of the output colors with the starting color
    RGB_list = [s]
    # Calcuate a color at each evenly spaced value of t from 1 to n
    for t in range(1, n):
        # Interpolate RGB vector for color at the current value of t
        curr_vector = [
        int(s[j] + (float(t)/(n-1))*(f[j]-s[j]))
            for j in range(3)
        ]
        # Add it to our list of output colors
        RGB_list.append(curr_vector)

    return color_dict_fn(RGB_list)

def polylinear_gradient(colors, n):
    ''' returns a list of colors forming linear gradients between
    all sequential pairs of colors. "n" specifies the total
    number of desired output colors '''
    # The number of colors per individual linear gradient
    n_out = int(float(n) / (len(colors) - 1))
    # returns dictionary defined by color_dict()
    gradient_dict = linear_gradient(colors[0], colors[1], n_out)

    if len(colors) > 1:
        for col in range(1, len(colors) - 1):
            next = linear_gradient(colors[col], colors[col+1], n_out)
            for k in ("hex", "r", "g", "b"):
                # Exclude first point to avoid duplicates
                gradient_dict[k] += next[k][1:]

    return gradient_dict

def make_cmap(list_of_colours, N=1000):
    interpolated_colors = polylinear_gradient(list_of_colours, n_colors)
    cmap = mcolors.ListedColormap([[interpolated_colors['r'][i]/256, interpolated_colors['g'][i]/256, interpolated_colors['b'][i]/256] for i in range(n_colors-5)])
    return cmap

def main():
    bit_cmap_dark = make_cmap([color_dict['dark_blue'], color_dict['blue'], color_dict['pink'],  color_dict['orange'], color_dict['red']])
    bit_cmap_light = make_cmap([color_dict['green'], color_dict['blue'], color_dict['sand'], color_dict['pink'],color_dict['orange']])

    pickle.dump(bit_cmap_dark, open('bit_cmap_dark.pkl', 'wb'))
    pickle.dump(bit_cmap_light, open('bit_cmap_light.pkl', 'wb'))

if __name__ == '__main__':
    main()