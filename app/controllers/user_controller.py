from flask import request
from app.validators.user import UserForm, PasswordForm
from app.handlers.response import success_response, error_response
from server import bcrypt, db
from app.models.user_model import UserModel
from app.models.password_model import PasswordModel
from app.models.backlisted_jwt_token_model import BlacklistedTokenModel
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt


def createUserController():
    try:
        # Parse JSON data from the request
        json_data = request.get_json()

        # Initialize the UserForm with JSON data
        userForm = UserForm(data=json_data)
        passwordForm = PasswordForm(
            data={"password": json_data.get("password")})

        if not userForm.validate() or not passwordForm.validate():
            # Form is not valid, return validation errors
            return error_response(userForm.errors or passwordForm.errors, 400)

        email = json_data["email"]

        if UserModel.query.filter_by(email=email).first():
            return error_response("User already exists", 409)

        hashed_password = bcrypt.generate_password_hash(json_data["password"])

        new_user = UserModel(full_name=json_data["full_name"], email=email)
        db.session.add(new_user)

        # Create the user and flush the session to get the user_id
        # This approach reduces the number of commits to one, ensuring that either both the user
        # and password are added to the database successfully, or no changes are made if an error occurs.
        # If an exception is raised, the code rolls back the transaction to maintain data integrity.
        db.session.flush()
        user_id = new_user.id

        new_user_password = PasswordModel(user_id, hashed_password)
        db.session.add(new_user_password)
        db.session.commit()

        user_dict = new_user.as_dict()

        return success_response(data=user_dict, message="Registration completed, kindly login.")

    except Exception as e:
        # Handle any exceptions that occur during processing or validation
        db.session.rollback()  # Rollback changes in case of an error
        return error_response(f"Something went wrong ({str(e)})", 500)


def loginUserController():
    try:
        json_data = request.get_json()
        email = json_data["email"]
        password = json_data["password"]

        # Authenticate user (you may need to retrieve the hashed password from your database)
        user = UserModel.query.filter_by(email=email).first()

        if user is None:
            return error_response("Invalid credentials", 400)

        user_dict = user.as_dict()
        userId = str(user_dict["id"])
        passwordInstance = PasswordModel.query.filter_by(
            user_id=userId).first()

        # Convert the hexadecimal string to bytes
        bytes_hashed_password = bytes.fromhex(
            passwordInstance.password[2:])  # Remove the leading "\\x"

        if user and bcrypt.check_password_hash(bytes_hashed_password, password.encode('utf-8')):
            # User is authenticated, create an access token

            access_token = create_access_token(identity=userId)
            return success_response({"access_token": access_token, "user_id": userId})

        return error_response("Invalid credentials", 401)

    except Exception as e:
        return error_response(f"Something went wrong ({str(e)})", 500)


def getUserController():
    try:
        current_user_id = get_jwt_identity()
        user = UserModel.query.filter_by(id=current_user_id).first()
        user_dict = user.as_dict()

        return success_response(user_dict)

    except Exception as e:
        return error_response(f"Something went wrong ({str(e)})", 500)


def logoutUserController():
    # Get the user's identity (user_id) from the JWT token
    jti = get_jwt()["jti"]
    # Extra security: The token has been added to a blacklist to prevent its future use
    blacklisted_token = BlacklistedTokenModel(jti=jti)
    db.session.add(blacklisted_token)
    db.session.commit()
    return success_response({"action": "User logged out successfully"})
