from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse, Response
from sqlalchemy.orm import Session
from io import BytesIO
import qrcode
import zipfile

from database import get_db
from models import Asset

router = APIRouter(prefix="/api/qrcode", tags=["QR Code"])

BASE_ASSET_URL = "http://192.168.0.189:3001/assets/"


def _generate_qr_image(data: str, box_size: int = 8) -> BytesIO:
    """生成 QR Code PNG 圖片，回傳 BytesIO 串流"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=2,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


@router.get("/{asset_id}")
def get_asset_qrcode(asset_id: int, db: Session = Depends(get_db)):
    """取得單一資產的 QR Code 圖片 (PNG)"""
    asset = db.query(Asset).filter(Asset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="資產不存在")

    url = f"{BASE_ASSET_URL}{asset.id}"
    buf = _generate_qr_image(url, box_size=10)

    return StreamingResponse(
        buf,
        media_type="image/png",
        headers={
            "Content-Disposition": f'attachment; filename="qrcode_{asset.asset_code}.png"',
        },
    )


@router.get("/batch/download")
def batch_download_qrcodes(db: Session = Depends(get_db)):
    """批次下載所有資產的 QR Code (ZIP 壓縮檔)"""
    assets = db.query(Asset).order_by(Asset.asset_code).all()
    if not assets:
        raise HTTPException(status_code=404, detail="沒有任何資產資料")

    zip_buf = BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for asset in assets:
            url = f"{BASE_ASSET_URL}{asset.id}"
            img_buf = _generate_qr_image(url, box_size=8)
            zf.writestr(f"qrcode_{asset.asset_code}.png", img_buf.getvalue())

    zip_buf.seek(0)
    return Response(
        content=zip_buf.getvalue(),
        media_type="application/zip",
        headers={
            "Content-Disposition": "attachment; filename=\"qrcodes_all.zip\"",
        },
    )


@router.get("/batch/preview")
def batch_preview_qrcodes(db: Session = Depends(get_db)):
    """取得所有資產的 QR Code 資訊 (用於前端批次展示)"""
    assets = db.query(Asset).order_by(Asset.asset_code).all()
    result = []
    for a in assets:
        result.append({
            "id": a.id,
            "asset_code": a.asset_code,
            "asset_name": a.asset_name,
            "category": a.category,
            "status": a.status,
            "qr_url": f"{BASE_ASSET_URL}{a.id}",
            "qr_api": f"/api/qrcode/{a.id}",
        })
    return result
