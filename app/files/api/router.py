"""Routes for file operations."""

from typing import Optional

import aiohttp
from fastapi import APIRouter, Body, File, Header, HTTPException, UploadFile
from pydantic import BaseModel
from app.files.infraestructura.minio.files_minio_persistece_service import FilesMinioPersisteceService

from app.files.dependency_injection.domain.create_file_controller import (
    CreateFileControllers,
)
from app.files.dependency_injection.domain.delete_file_controller import (
    DeleteFileControllers,
)
from app.files.dependency_injection.domain.get_file_controller import (
    GetFileControllers,
)
from app.files.dependency_injection.domain.list_files_controller import (
    ListFilesControllers,
)
from app.files.dependency_injection.domain.merge_files_controller import (
    MergeFilesControllers,
)
from app.files.dependency_injection.domain.update_file_content_controller import (
    UpdateFileContentControllers,
)
from app.files.domain.exceptions.FileNotFoundException import FileNotFoundException
from app.files.domain.exceptions.UnauthorizedFileAccessException import (
    UnauthorizedFileAccessException,
)

router = APIRouter(prefix="/files", tags=["files"])

# ============================================================================
# Helper function to get user_id from authentication service
# ============================================================================
async def get_user_from_token(token: str) -> int:
    url = "http://localhost:80/authentication/introspect"
    headers = {"auth": token, "content-type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise HTTPException(status_code=403, detail="Forbidden")
            data = await response.json()
            if "user_id" not in data:
                raise HTTPException(status_code=403, detail="Forbidden")
            return data["user_id"]

# ============================================================================
# Pydantic Models
# ============================================================================
class FileResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    content_path: Optional[str] = None
    original_filename: Optional[str] = None
    user_id: int

class CreateFileRequest(BaseModel):
    title: str
    description: Optional[str] = None

class CreateFileResponse(BaseModel):
    id: int

class GetFileResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    content_path: Optional[str] = None
    original_filename: Optional[str] = None
    user_id: int

class MergeFilesRequest(BaseModel):
    """Request model for merging files."""

    file_ids: list[int]


class MergeFilesResponse(BaseModel):
    """Response model for merging files."""

    id: int

class StatusResponse(BaseModel):

    status: str

# ============================================================================
# GET /files - List all files for the authenticated user
# ============================================================================

@router.get("", response_model=list[FileResponse])
async def list_files(auth: str = Header()) -> list[FileResponse]:
    """List all files owned by the authenticated user."""
    user_id = await get_user_from_token(auth)
    list_controller = ListFilesControllers.carlemany()
    files_bo = await list_controller(user_id=user_id)
    return [
        FileResponse(
            id=f.id,
            title=f.title,
            description=f.description,
            content_path=f.content_path,
            original_filename=f.original_filename,
            user_id=f.user_id,
        )
        for f in files_bo
    ]


# ============================================================================
# POST /files - Create a new file (metadata only)
# ============================================================================

@router.post("", response_model=CreateFileResponse)
async def create_file(auth: str = Header(), body: CreateFileRequest = Body()) -> CreateFileResponse:
    """Create a new file (metadata only)."""
    user_id = await get_user_from_token(auth)
    create_controller = CreateFileControllers.carlemany()
    file_bo = await create_controller(
        title=body.title,
        description=body.description or "",
        user_id=user_id,
    )
    return CreateFileResponse(id=file_bo.id)


# ============================================================================
# GET /files/{file_id} - Get file by ID
# ============================================================================

@router.get("/{file_id}", response_model=GetFileResponse)
async def get_file(file_id: int, auth: str = Header()) -> GetFileResponse:
    """Get a specific file by ID."""
    user_id = await get_user_from_token(auth)
    get_controller = GetFileControllers.carlemany()
    try:
        file_bo = await get_controller(file_id=file_id, user_id=user_id)
    except FileNotFoundException:
        raise HTTPException(status_code=404, detail="File not found") from None
    except UnauthorizedFileAccessException:
        raise HTTPException(status_code=403, detail="Forbidden") from None

    return GetFileResponse(
        id=file_bo.id,
        title=file_bo.title,
        description=file_bo.description,
        content_path=file_bo.content_path,
        original_filename=file_bo.original_filename,
        user_id=file_bo.user_id,
        path=files_persistence_service.get_file(current_file.path)
    )


# ============================================================================
# POST /files/merge - Merge multiple PDF files
# ============================================================================

@router.post("/merge", response_model=MergeFilesResponse)
async def merge_files(auth: str = Header(), body: MergeFilesRequest = Body()) -> MergeFilesResponse:
    """Merge multiple PDF files."""
    user_id = await get_user_from_token(auth)
    merge_controller = MergeFilesControllers.carlemany()
    try:
        merged_file_id = await merge_controller(file_ids=body.file_ids, user_id=user_id)
    except FileNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e)) from None
    except UnauthorizedFileAccessException:
        raise HTTPException(status_code=403, detail="Forbidden") from None

    return MergeFilesResponse(id=merged_file_id)


# ============================================================================
# POST /files/{file_id} - Upload file content
# ============================================================================
@router.post("/{file_id}", response_model=StatusResponse)
async def update_file_content(
    file_id: int,
    auth: str = Header(),
    content: UploadFile = File(...),
    datebase_file.path = files_persistence_service.store(relative_path)
    os.remove(relative_path)
) -> StatusResponse:
    """Upload/update content for a specific file."""
    user_id = await get_user_from_token(auth)
    update_controller = UpdateFileContentControllers.carlemany()
    try:
        await update_controller(file_id=file_id, user_id=user_id, upload_file=content)
    except FileNotFoundException:
        raise HTTPException(status_code=404, detail="File not found") from None
    except UnauthorizedFileAccessException:
        raise HTTPException(status_code=403, detail="Forbidden") from None

    return StatusResponse(status="ok")


# ============================================================================
# DELETE /files/{file_id} - Delete a file
# ============================================================================
@router.delete("/{file_id}", response_model=StatusResponse)
async def delete_file(file_id: int, auth: str = Header()) -> StatusResponse:
    """Delete a specific file."""
    user_id = await get_user_from_token(auth)
    delete_controller = DeleteFileControllers.carlemany()
    try:
        await delete_controller(file_id=file_id, user_id=user_id)
    except FileNotFoundException:
        raise HTTPException(status_code=404, detail="File not found") from None
    except UnauthorizedFileAccessException:
        raise HTTPException(status_code=403, detail="Forbidden") from None

    return StatusResponse(status="ok")

# ============================================================================
# DELETE /files/{file_id} - Delete a file
# ============================================================================
files_persistence_service = FilesMinioPersisteceService()