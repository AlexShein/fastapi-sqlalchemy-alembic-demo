from fastapi import status


def test_users(client):  # noqa: F811
    # Create a user
    response = client.post(
        "/users",
        json={"email": "alex@iceye.fi", "is_active": True},
    )
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    user_id = body["id"]

    response = client.get("/users")
    print("####", response.json())
    # Fetch user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK


def test_user_notes(client):  # noqa: F811
    # Create a user
    response = client.post(
        "/users",
        json={"email": "alex@iceye.fi", "is_active": True},
    )
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    user_id = body["id"]
    # Fetch user
    response = client.post(
        f"/users/{user_id}/notes",
        json={"title": "New note", "description": "Some description"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    note_id = body["id"]

    # Fetch note
    response = client.get(f"/users/{user_id}/notes")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()

    assert len(body) == 1
    assert body[0]["id"] == note_id

    # Fetch user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()

    assert len(body["notes"]) == 1


def test_notes(client):  # noqa: F811
    # Create a user
    response = client.post(
        "/users",
        json={"email": "alex@iceye.fi", "is_active": True},
    )
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    user_id = body["id"]
    # Create a note
    response = client.post(
        "/notes",
        json={
            "title": "New note",
            "description": "Some description",
            "user_id": user_id,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    note_id = body["id"]

    # Fetch notes
    response = client.get("/notes")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()

    assert len(body) == 1
    assert body[0]["id"] == note_id

    # Fetch user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()

    assert len(body["notes"]) == 1


def test_documents(client):  # noqa: F811
    # Create a user
    response = client.post(
        "/users",
        json={"email": "alex@iceye.fi", "is_active": True},
    )
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    user_id = body["id"]

    # Create an inactive user
    response = client.post(
        "/users",
        json={"email": "someone.else@iceye.fi", "is_active": False},
    )
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    inactive_user_id = body["id"]

    # Create a document
    response = client.post(
        "/documents",
        json={
            "title": "New doc",
            "content": "Some content",
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    document_id = body["id"]

    # Create a user-document relation entry
    response = client.post(
        "/user-documents",
        json={
            "user_id": user_id,
            "document_id": document_id,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Create a user-document relation entry for an inactive user
    response = client.post(
        "/user-documents",
        json={
            "user_id": inactive_user_id,
            "document_id": document_id,
        },
    )
    assert response.status_code == status.HTTP_201_CREATED

    # Fetch document
    response = client.get(f"/documents/{document_id}")
    assert response.status_code == status.HTTP_200_OK
    body = response.json()

    assert len(body["users"]) == 1
    assert body["users"][0]["id"] == user_id
