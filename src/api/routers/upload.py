from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from garmin_ai.config import DATA_DIR

router = APIRouter()

@router.post("/upload")
async def upload_files(
    activities: UploadFile = File(...),
    splits: UploadFile = File(...),
    fit: UploadFile = File(...)
):
    """
    Upload Garmin files and save them into DATADIR/csv and DATADIR/fit.
    """

    csv_dir = DATA_DIR / "csv"
    fit_dir = DATA_DIR / "fit"
    csv_dir.mkdir(parents=True, exist_ok=True)
    fit_dir.mkdir(parents=True, exist_ok=True)

    # Save Activities.csv
    activities_path = csv_dir / "Activities.csv"
    with open(activities_path, "wb") as f:
        f.write(await activities.read())

    # Save splits.csv
    splits_path = csv_dir / "splits.csv"
    with open(splits_path, "wb") as f:
        f.write(await splits.read())

    # Save .fit file
    fit_path = fit_dir / fit.filename
    with open(fit_path, "wb") as f:
        f.write(await fit.read())

    return {"status": "files uploaded"}
