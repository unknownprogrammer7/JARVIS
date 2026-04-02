class PermissionsManager:
    """
    A class to manage permissions for J.A.R.V.I.S.

    This class handles the assignment and verification of permissions
    for different roles in the system, ensuring that users have
    appropriate access to various functionalities.

    Attributes:
    ----------
    permissions : dict
        A dictionary mapping roles to their permissions.
    
    Methods:
    -------
    assign_permission(role: str, permission: str) -> None:
        Assigns a permission to a specified role.
    
    remove_permission(role: str, permission: str) -> None:
        Removes a permission from a specified role.
    
    check_permission(role: str, permission: str) -> bool:
        Checks if a specified role has a certain permission.
    
    list_permissions(role: str) -> list:
        Lists all permissions assigned to a specified role.
    """

    def __init__(self):
        """
        Initializes the PermissionsManager with default permissions.
        """
        self.permissions = {
            'admin': [],
            'user': [],
            'guest': []
        }

    def assign_permission(self, role: str, permission: str) -> None:
        """
        Assigns a permission to a specified role.
        
        Parameters:
        ----------
        role : str
            The role to assign the permission to.
        permission : str
            The permission to be assigned.
        """
        if role in self.permissions:
            self.permissions[role].append(permission)
        else:
            raise ValueError(f'Role {role} does not exist.')

    def remove_permission(self, role: str, permission: str) -> None:
        """
        Removes a permission from a specified role.
        
        Parameters:
        ----------
        role : str
            The role to remove the permission from.
        permission : str
            The permission to be removed.
        """
        if role in self.permissions:
            try:
                self.permissions[role].remove(permission)
            except ValueError:
                raise ValueError(f'Permission {permission} not found for role {role}.')
        else:
            raise ValueError(f'Role {role} does not exist.')

    def check_permission(self, role: str, permission: str) -> bool:
        """
        Checks if a specified role has a certain permission.
        
        Parameters:
        ----------
        role : str
            The role to check permissions for.
        permission : str
            The permission to check.
        
        Returns:
        -------
        bool
            True if the role has the permission, False otherwise.
        """
        return permission in self.permissions.get(role, [])

    def list_permissions(self, role: str) -> list:
        """
        Lists all permissions assigned to a specified role.
        
        Parameters:
        ----------
        role : str
            The role to list permissions for.
        
        Returns:
        -------
        list
            A list of permissions assigned to the role.
        """
        return self.permissions.get(role, [])
