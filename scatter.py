import numpy as np
import pandas as pd
import matplotplib.pyplot as plt
from seaborn import hls_palette, color_palette

def plt_scatter2d(df, ax=None,s=1, alpha=1,
                  color=None, cmap=None, palette=None, color_order=None,
                  label_prefix=None, xylabels=None, title=None,
                  legend=True, bbox_anchor=(1,1),
                  replace_colors=None, legend_ncol=1,
                  figsize=(4.5,4),  vmin=None, vmax=None) :
    
    if ax is None:
        fig, ax = plt.subplots(figsize=figsize)
    else :
        fig = None
    
    if isinstance(df,pd.core.frame.DataFrame) :
        x = df.iloc[:,0]
        y = df.iloc[:,1]
    else :
        x = df[:,0]
        y = df[:,1]
    
    if isinstance(color, (list,pd.core.series.Series,np.ndarray)) :
        cat_types = ["str"]
        if isinstance(color, pd.core.series.Series) :
            #cat_types.append("category")
            cat_types.append("object")

        if color.dtype in cat_types or hasattr(color, 'cat') :
            if cmap is None :
                color_order = np.unique(color) if color_order is None else color_order
                if palette is None :
                    palette = hls_palette(len(color_order))
                else : 
                    palette = color_palette(palette, len(color_order))
                cmap = dict(zip(color_order,palette))
                
                if not replace_colors is None :
                    for key,col in replace_colors.items() :
                        cmap[key] = col

    sc = ax.scatter(x, y, 
                    s=s, alpha=alpha, 
                    cmap=palette,
                    c=color if cmap is None else [cmap[i] for i in color],
                    lw=0,
                    rasterized = True,
                    vmin=vmin, vmax=vmax)

    ax.set_xticks([])
    ax.set_yticks([])
    if not label_prefix is None :
        ax.set_ylabel("{}2".format(label_prefix))
        ax.set_xlabel("{}1".format(label_prefix))
    else :
        if xylabels is None and isinstance(df,pd.core.frame.DataFrame) :
            ax.set_xlabel(df.columns[0])
            ax.set_ylabel(df.columns[1])
    ax.set_title(title)

    
    if isinstance(color, (list,pd.core.series.Series,np.ndarray)) :
        cat_types = ["str"]
        if isinstance(color, pd.core.series.Series) :
            #cat_types.append("category")
            cat_types.append("object")

        if color.dtype in cat_types or hasattr(color, 'cat') and legend == True :
            handles = [
                matplotlib.lines.Line2D(
                    [],
                    [],
                    marker="o",
                    color=color,
                    linewidth=0,
                    label=label,
                    markersize=10,
                )
                for label, color in cmap.items()
            ]
            ax_legend = ax.legend(
                handles=handles,
                bbox_to_anchor=bbox_anchor,
                fontsize="x-small",
                ncol=legend_ncol,
            )
        else :
            cbar = plt.gcf().colorbar(sc, 
                                      pad=0, 
                                      ax=ax,
                                      fraction=0.15 if legend == True else 1e-7,
                                      ticks=None if legend==True else [])

    if fig is None :
        return ax
    else :
        plt.show()
        return fig, ax
