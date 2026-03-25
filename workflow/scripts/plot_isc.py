from nilearn import plotting

isc_nii = snakemake.input["isc_nii"]
png_file = snakemake.output["png"]
html_file = snakemake.output["html"]

print(f"Plotting ISC map: {isc_nii}")

# Static PNG
display = plotting.plot_stat_map(
    isc_nii,
    title=f"Mean ISC - Task '{snakemake.wildcards.task}'",
    display_mode="ortho",
    cut_coords=(0, -20, 40),
    colorbar=True
)
display.savefig(png_file)
display.close()

# Interactive HTML
view = plotting.view_img(isc_nii, title=f"Mean ISC - Task '{snakemake.wildcards.task}'")
view.save_as_html(html_file)

print(f"Saved plots: {png_file}, {html_file}")