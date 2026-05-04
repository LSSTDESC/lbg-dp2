import os

from ceci.config import StageParameter
from rail.core.data import PqHandle
from rail.core.stage import RailStage
from rail.projects.reducer import FlagshipReducer as RailFlagshipReducer


class FlagshipReducer(RailStage):
    """Load Flagship simulation pixel files and reduce to a standard catalog.

    Wraps FlagshipReducer from rail_projects to convert raw per-pixel parquet
    files (flux columns, Flagship coordinate convention) into a reduced catalog
    with AB magnitudes and standard ra/dec.  The output is a single parquet
    file suitable for downstream RAIL degradation stages.
    """

    name = "FlagshipReducer"
    inputs = []
    outputs = [("output_catalog", PqHandle)]
    config_options = RailStage.config_options.copy()
    config_options.update(
        dict(
            input_dir=StageParameter(
                str,
                "/global/cfs/cdirs/lsst/groups/PZ/Flagship/Roman",
                msg="Directory containing Flagship pixel parquet files (wNIR)",
            ),
            pixels=StageParameter(
                list,
                [27, 28, 35, 36, 43, 44],
                msg="HEALPix pixel IDs to load",
            ),
            file_pattern=StageParameter(
                str,
                "euclid_fs2_mock_dr_v1_1_phz_wNIR.pix{pixel}.pq",
                msg="Filename pattern; {pixel} is replaced with each pixel ID",
            ),
            cuts=StageParameter(
                dict,
                {"maglim_i": [None, 99.0]},
                msg="Magnitude/column cuts passed to FlagshipReducer",
            ),
        )
    )

    def run(self):
        pixel_files = [
            os.path.join(
                self.config.input_dir,
                self.config.file_pattern.format(pixel=p),
            )
            for p in self.config.pixels
        ]
        # Write to the inprogress path; _finalize_tag will rename it.
        out_path = self.get_output("output_catalog", final_name=False)
        reducer = RailFlagshipReducer(name="flagship_reducer", cuts=self.config.cuts)
        reducer.run(pixel_files, out_path)

    def _finalize_tag(self, tag):
        # RailFlagshipReducer.run() writes directly to disk and returns None, so
        # RAIL's handle never receives data.  Skip handle.write() and delegate to
        # ceci's rename logic (inprogress_ → final name) instead.
        from ceci.stage import PipelineStage

        final_name = PipelineStage._finalize_tag(self, tag)
        handle = self.get_handle(tag, allow_missing=True)
        if handle is not None:
            handle.path = final_name
        return final_name
