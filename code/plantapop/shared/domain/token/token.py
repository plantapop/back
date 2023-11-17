import jose


class Token:
    def __init__(
        self,
        token: str,
        user_uuid: str,
        token_type: str,
        device: str,
        duration: int,
        revoked: bool,
    ):
        self.token = token
        self.user_uuid = user_uuid
        self.token_type = token_type
        self.device = device
        self.duration = duration
        self.revoked = revoked

    @classmethod
    def create(
        cls,
        user_uuid: str,
        token_type: str,
        device: str,
        duration: int,
        algorithm: str,
        key: str,
        revoked: bool = False,
    ) -> str:
        token = jose.jwt.encode(
            {
                "exp": duration,
                "uuid": user_uuid,
                "type": token_type,
                "device": device,
            },
            key,
            algorithm=algorithm,
        )

        return cls(token, user_uuid, token_type, device, duration, revoked)

    def revoke(self) -> None:
        self.revoked = True

    def is_revoked(self) -> bool:
        return self.revoked

    def get(self) -> str:
        return self.token

    def get_user_uuid(self) -> str:
        return self.user_uuid
