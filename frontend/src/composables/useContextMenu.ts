import { ref, computed } from 'vue';

export interface MenuItem {
  key: string;
  label: string;
  icon?: any; // Component type
  variant?: 'default' | 'danger';
  checked?: boolean;
  disabled?: boolean;
  action?: () => void;
}

export interface Position {
  x: number;
  y: number;
}

export function useContextMenu() {
  const contextMenuVisible = ref(false);
  const menuPosition = ref<Position>({ x: 0, y: 0 });
  const menuItems = ref<MenuItem[]>([]);
  const targetElement = ref<HTMLElement | null>(null);

  const showContextMenu = (items: MenuItem[], element?: HTMLElement) => {
    menuItems.value = items;
    targetElement.value = element || null;
    contextMenuVisible.value = true;
  };

  const hideContextMenu = () => {
    contextMenuVisible.value = false;
    menuItems.value = [];
    targetElement.value = null;
  };

  const handleMenuItemClick = (item: MenuItem) => {
    if (!item.disabled && item.action) {
      item.action();
    }
    hideContextMenu();
  };

  return {
    contextMenuVisible,
    menuPosition,
    menuItems,
    targetElement,
    showContextMenu,
    hideContextMenu,
    handleMenuItemClick,
  };
}