from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# TODO replace email str with EmailStr when sqlmodel supports it
class UserCreateOpen(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    profile: list["Profile"] = Relationship(back_populates="user")
    rooms: list["Room"] = Relationship(back_populates="owner")
    items: list["Item"] = Relationship(back_populates="owner")
    section: list["Section"] = Relationship(back_populates="owner")
    collection: list["Collection"] = Relationship(back_populates="owner")
    question: list["Question"] = Relationship(back_populates="owner")
    modules: list["Module"] = Relationship(back_populates="owner")
    badges: list["Badges"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int


class UsersOut(SQLModel):
    data: list[UserOut]
    count: int


class ProfileBase(SQLModel):
    full_name: str
    country: str
    rank: int
    level: int
    bio: str
    github_link: str
    linkedin_link: str
    personal_blog_link: str
    job: str
    active_room: bool
    completed_rooms: str
    friends: str
    badges: str
    created_rooms: str


class ProfileCreate(ProfileBase):
    full_name: str
    country: str
    rank: int
    level: int
    bio: str
    github_link: str
    linkedin_link: str
    personal_blog_link: str
    job: str
    active_room: bool
    completed_rooms: str
    friends: str
    badges: str
    created_rooms: str


class ProfileUpdate(ProfileBase):
    full_name: str | None = None
    country: str | None = None
    rank: int | None = None
    level: int | None = None
    github_link: str | None = None
    linkedin_link: str | None = None
    personal_blog_link: str | None = None
    job: str | None = None
    active_room: bool | None = None
    completed_rooms: str | None = None
    friends: str | None = None
    created_rooms: str | None = None


class Profile(ProfileBase, table=True):
    id: UUID | None = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    user_id: int = Field(foreign_key="user.id", nullable=False)
    # O-O relationship
    user: User = Relationship(
        sa_relationship_kwargs={
            "uselist": False
        },  # SQLModel is a wrapper around SQLAlchemy, so you can use SQLAlchemy's relationship kwargs
        back_populates="profile",
    )


class ProfileOut(ProfileBase):
    id: UUID
    user_id: int

################################ Room ##########################
class RoomBase(SQLModel):
    title: str
    description: str | None = None
    difficulty: int
    is_active: bool
    recommended_video: str | None = None
    room_type: str
    visibility: str
    created_at: str
    updated_at: str
    deleted_at: str | None = None
    file_name: str = None


class RoomCreate(RoomBase):
    title: str
    description: str | None = None
    difficulty: int
    is_active: bool
    recommended_video: str | None = None
    room_type: str
    visibility: str
    created_at: str
    updated_at: str
    deleted_at: str | None = None
    file_name: str = None


class RoomUpdate(RoomBase):
    title: str | None = None
    description: str | None = None
    difficulty: int | None = None
    is_active: bool | None = None
    recommended_video: str | None = None
    room_type: str | None = None
    visibility: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    file_name: str = None


class Room(RoomBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="rooms")


class RoomOut(RoomBase):
    id: int
    owner_id: int | None = None


class RoomsOut(SQLModel):
    data: list[RoomOut]
    count: int

###################### section ##################
class SectionBase(SQLModel):
    id : int
    title: str = None
    Content: str
    questions: str
    
class SectionCreate(SectionBase):
    id : int
    title: str = None
    Content: str
    questions: str


class SectionUpdate(SectionBase):
    id : int  | None = None
    title: str | None = None
    Content: str |None = None
    questions: str |None = None


class Section(SectionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="section")


class SectionOut(SectionBase):
    id: int
    owner_id: int | None = None


class SectionsOut(SQLModel):
    data: list[SectionOut]
    count: int
###################### collection ##################
class CollectionBase(SQLModel):
    id : int
    title: str = None
    description: str
    rooms: str
    
class CollectionCreate(CollectionBase):
    id : int
    title: str = None
    description: str
    rooms: str


class CollectionUpdate(CollectionBase):
    id : int  | None = None
    title: str | None = None
    description: str |None = None
    rooms: str |None = None


class Collection(CollectionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="collection")


class CollectionOut(CollectionBase):
    id: int
    owner_id: int | None = None


class CollectionsOut(SQLModel):
    data: list[CollectionOut]
    count: int
######################  Question ##################
class QuestionBase(SQLModel):
    id : int
    content: str = None
    answer: str
    hint: str
    
class QuestionCreate(QuestionBase):
    id : int
    content: str = None
    answer: str
    hint: str


class QuestionUpdate(QuestionBase):
    id : int  | None = None
    content: str | None = None
    answer: str |None = None
    hint: str |None = None


class Question(QuestionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="question")


class QuestionOut(QuestionBase):
    id: int
    owner_id: int | None = None


class QuestionsOut(SQLModel):
    data: list[QuestionOut]
    count: int
######################  Moduels ##################
class ModuleBase(SQLModel):
    id : int
    level : int
    description: str
    author: str
    created_at : str
    visibility : bool
    collection: str

    
class ModuleCreate(ModuleBase):
    id : int
    level : int
    created_at : str
    description: str = None
    author: str
    visibility : bool
    collection: str


class ModuleUpdate(ModuleBase):
    id : int | None = None
    level : int | None = None
    author: str | None = None
    created_at : str | None = None
    description: str | None = None
    visibility : bool | None = None
    collection: str | None = None


class Module(ModuleBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="modules")


class ModuleOut(ModuleBase):
    id: int
    owner_id: int | None = None


class ModuelsOut(SQLModel):
    data: list[ModuleOut]
    count: int
######################  Badges ##################
class BadgesBase(SQLModel):
    id : int
    title: str = None
    image: str
    
    
class BadgesCreate(BadgesBase):
    id : int
    title: str = None
    image: str
    


class BadgesUpdate(BadgesBase):
    id : int  | None = None
    title: str | None = None
    image: str |None = None
    


class Badges(BadgesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="badges")


class BadgesOut(BadgesBase):
    id: int
    owner_id: int | None = None


class BadgessOut(SQLModel):
    data: list[BadgesOut]
    count: int



# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str

# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemOut(ItemBase):
    id: int
    owner_id: int


class ItemsOut(SQLModel):
    data: list[ItemOut]
    count: int
