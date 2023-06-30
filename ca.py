import math
import matplotlib.pyplot as plt
import numpy as np


def update_grid(grid, on=255, off=0):
    # copy grid since we require 8 neighbors
    # for calculation and we go line by line
    new_grid = np.zeros_like(grid)
    nrows = grid.shape[0]
    ncols = grid.shape[1]
    for i in range(nrows):
        for j in range(ncols):
            # Compute 8-neighbor sum using toroidal boundary
            # conditions: x and y wrap around so simulation takes
            # place on a toroidal surface (e.g. Pac-Man)
            # % is modulus; counts across rows as if rotary phone dial
            n_neighbors = (
                int(grid[(i-1) % nrows, (j-1) % ncols])
                + int(grid[(i-1) % nrows, j])
                + int(grid[(i-1) % nrows, (j+1) % ncols])
                + int(grid[i, (j-1) % ncols])
                + int(grid[i, (j+1) % ncols])
                + int(grid[(i+1) % nrows, (j-1) % ncols])
                + int(grid[(i+1) % nrows, j])
                + int(grid[(i+1) % nrows, (j+1) % ncols])
            ) // 255
            # Apply Conway's Game of Life rules
            if grid[i, j]  == on:
                # 1. Any live cell with fewer than two live neighbours dies,
                #    as if by underpopulation
                if n_neighbors < 2:
                    new_grid[i, j] = off
                # 2. Any live cell with two or three live neighbours lives on
                if (n_neighbors == 2) or (n_neighbors == 3):
                    new_grid[i, j] = on
                # 3. Any live cell with more than three live neighbours dies,
                #    as if by overpopulation
                if n_neighbors > 3:
                    new_grid[i, j] = off
            else:
                # 4. Any dead cell with exactly three live neighbours becomes
                #    a live cell, as if by reproduction
                if n_neighbors == 3:
                    new_grid[i, j] = on
    return new_grid

def plot_images(
    imgs,
    imgs_per_row='all',
    cmap='gray',
    fig_w=7.5,
    dpi=100
):
    """Plot images.
    ----------
    Parameters
    ----------
    imgs : list
        List of NumPy arrays representing images to be plotted.
    imgs_per_row : int or 'all', optional
        Number of images to plot in each row. Default is None and all images
        are plotted in the same row. Defaults to 'all'.
    fig_w : float, optional
        Width of figure in inches, by default 7.5
    dpi : float, optional
        Resolution (dots per inch) of figure. Defaults to 300.
    -------
    Returns
    -------
    matplotlib.Figure, matplotlib.Axis
        2-tuple containing matplotlib figure and axes objects
    """
    # If single image passed, add it to a list
    if not isinstance(imgs, list):
        imgs = [imgs]
    n_imgs = len(imgs)
    img_w = imgs[0].shape[1]
    img_h = imgs[0].shape[0]
    if imgs_per_row == 'all':
        n_cols = n_imgs
    else:
        n_cols = imgs_per_row
    n_rows = int(math.ceil( n_imgs / n_cols ))
    fig_h = fig_w * (img_h / img_w) * (n_rows / n_cols)
    fig, axes = plt.subplots(
        n_rows, n_cols, figsize=(fig_w, fig_h), constrained_layout=True,
        dpi=dpi, facecolor='white'
    )
    if isinstance(axes, np.ndarray):
        ax = axes.ravel()
    else:
        # When only one image, wrap axis object into list to make iterable
        ax = [axes]
    for i, img in enumerate(imgs):
        ax[i].imshow(img, cmap='gray', interpolation='nearest')
        ax[i].axis('off')
    return fig, axes