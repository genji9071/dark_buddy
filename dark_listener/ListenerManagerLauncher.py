class ListenerManagerLauncher():
    def __init__(self):
        self.tenant_map = {}
        self.external_map = {}

    def set_current_listener_manager(self, user_id, tenant_id, listener_manager):
        from config import TenantConfig
        tenant_info = TenantConfig.tenant_base_info[tenant_id]
        if tenant_info['isExternal']:
            if user_id in self.external_map:
                self.external_map[user_id].delete(user_id, tenant_id)
            self.external_map[user_id] = listener_manager
        else:
            if tenant_id in self.tenant_map:
                self.tenant_map[tenant_id].delete(user_id, tenant_id)
            self.tenant_map[tenant_id] = listener_manager

    def get_current_listener_manager(self, request_json: dict):
        user_id = request_json['senderId']
        tenant_id = request_json['chatbotUserId']
        from config import TenantConfig
        tenant_info = TenantConfig.tenant_base_info[tenant_id]
        if tenant_info['isExternal']:
            return self.external_map.get(user_id)
        else:
            return self.tenant_map.get(tenant_id)


listener_manager_launcher = ListenerManagerLauncher()
