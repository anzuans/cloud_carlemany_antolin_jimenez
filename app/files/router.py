"""Routes for file operations."""
import uuid
from typing import Optional

from fastapi import APIRouter, Header, Body, HTTPException, UploadFile, File
import aiohttp
from pydantic import BaseModel
from pypdf import PdfMerger

router = APIRouter(prefix="/files", tags=["files"])

file_counter = -1
files_db = {}


class FilesBO(BaseModel):
    id: int
    title: str
    author: str
    email: str
    path: Optional[str] = None


class UserBO(BaseModel):
    email: str


async def introspect(token: str) -> UserBO:
    url = "http://localhostL:80/instrospect"
    headers = {"auth": token, "content-type": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise HTTPException(status_code=401, detail="Unauthorized")
            data = await response.json()
        return UserBO(email=data["email"])


def chek_ownership(user: UserBO, id: int) -> FilesBO:
    file = files_db[id]
    if user.email != file.email:
        raise HTTPException(status_code=403, detail="Unauthorized")

    return file


class FilesGet(BaseModel):
    id: int
    title: str
    author: str
    email: str
    path: Optional[str] = None


@router.get("")
async def files_get(auth: str = Header()) -> list[FilesGet]:
    """List files."""
    user = await introspect(auth)
    user_files = []

    for file in files_db:
        if user.email != file.email:
            user_files.append(file)

    return user_files


class FilesPostInput(BaseModel):
    title: str
    author: str


@router.post("")
async def files_post(auth: str = Header(), body: FilesPostInput = Body()) -> dict[str, int]:
    """Create a file."""
    user = await introspect(auth)
    global file_counter
    file_counter += 1

    current_file = FilesBO(title=body.title, author=body.author, id=file_counter, email=user.email)
    files_db[current_file.id] = current_file

    return {"id": current_file.id}


class MergePost(BaseModel):
    file_1_id: int
    file_2_id: int


@router.post("/merge")
async def files_merge_post(auth: str = Header(), body: MergePost = Body()) -> dict[str, int]:
    """Merge files."""
    user = await introspect(auth)
    current_file_1 = chek_ownership(user, body.file_1_id)
    current_file_2 = chek_ownership(user, body.file_2_id)

    if current_file_1.path is None or current_file_2.path is None:
        raise HTTPException(status_code=404, detail="File not found")

    file_1_name = current_file_1.path.split("/")[-1].split(".")[0]
    file_2_name = current_file_2.path.split("/")[-1].split(".")[0]
    file_name_result = f"files/{file_1_name}_{file_2_name}.pdf"

    merger = PdfMerger()

    pdfs = [current_file_1.path,
            current_file_2.path]
    for pdf in pdfs:
        merger.append(pdf)

    merger.write(file_name_result)

    merger.close()

    global files_counter
    files_counter += 1
    current_file = FilesBO(title=f"{file_1_name}_{file_2_name}",
                           author=f"{current_file_1.author}_{current_file_2.author}", id=file_counter, email=user.email,
                           path=file_name_result)
    files_db[current_file.id] = current_file

    return {"id": current_file.id}


class FilesIdGet(BaseModel):
    id: int
    title: str
    author: str
    email: str
    path: Optional[str] = None


@router.get("/{file_id}")
async def files_id_get(id: int, auth: str = Header()) -> FilesIdGet:
    """Get a file by ID."""
    user = await introspect(auth)
    current_file = chek_ownership(user, id)
    return FilesIdGet(id=id, title=current_file.title, author=current_file.author, path=current_file.path,
                      email=current_file.email)


@router.post("/{file_id}")
async def files_id_post(id: int, auth: str = Header(), file_content: UploadFile = File()) -> dict[str, int]:
    """Update a file by ID."""
    user = await introspect(auth)
    db_file = chek_ownership(user, id)
    prefix = "files/"
    relative_path = prefix + str(uuid.uuid4()) + ".pdf"

    with open(relative_path, "wb") as buffer:
        while chunk := await file_content.read(8192):
            buffer.write(chunk)

    db_file.path = relative_path

    return {"id": id}


@router.delete("/{file_id}")
async def files_id_delete(id: int, auth: str = Header()) -> dict[str, int]:
    """Delete a file by ID."""
    user = await introspect(auth)
    chek_ownership(user, id)
    del files_db[id]

    return {"id": id}
