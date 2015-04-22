/*********************************************************************
*	Copyright, 2008-2012, L-3 Communications Integrated Systems
*			All rights reserved.
*
*@author	jeggebre
*@version	6.0
*@date		Fri Sep 21 07:24:47 CDT 2012
*@file		Crowbar.java
**********************************************************************/
package com.l3is.waco.crowbar.main;

import gen.module.CommandType;
import gen.module.ItemType;
import gen.roles.RoleList.Role;
import gen.servers.ServerType;
import gen.module.StepType;
import gen.servers.BayType;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Component;
import java.awt.ComponentOrientation;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.Insets;
import java.awt.Rectangle;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.KeyboardFocusManager;
import java.awt.datatransfer.DataFlavor;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.IOException;
import java.io.PrintStream;
import java.lang.reflect.Constructor;
import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Observable;
import java.util.Observer;
import java.util.concurrent.locks.ReentrantLock;
import java.util.logging.Logger;

import javax.swing.Action;
import javax.swing.ActionMap;
import javax.swing.Box;
import javax.swing.BoxLayout;
import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JCheckBoxMenuItem;
import javax.swing.JDesktopPane;
import javax.swing.JFrame;
import javax.swing.JInternalFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JScrollPane;
import javax.swing.JSeparator;
import javax.swing.JSplitPane;
import javax.swing.JTextPane;
import javax.swing.SwingUtilities;
import javax.swing.text.DefaultEditorKit;
import javax.swing.text.JTextComponent;
import javax.swing.JToolBar;

import javax.swing.WindowConstants;
import javax.swing.border.BevelBorder;
import javax.swing.border.EmptyBorder;
import javax.swing.event.MenuEvent;
import javax.swing.event.MenuListener;

import com.l3is.waco.crowbar.controller.CrowbarController;
import com.l3is.waco.crowbar.util.CrowbarCommand;
import com.l3is.waco.crowbar.util.CrowbarLDAP;
import com.l3is.waco.crowbar.util.CrowbarUser;
import com.l3is.waco.crowbar.util.CrowbarNetworkStatusChecker;
import com.l3is.waco.crowbar.util.EncryptUtil;
import com.l3is.waco.crowbar.util.UpsStatusChecker;
import com.l3is.waco.crowbar.view.widget.CrowbarDropButton;
import com.swtdesigner.SwingResourceManager;

/**
 * This is the main starting point for CROWBAR. This class creates the main menu and toolbar for CROWBAR.
 * @author combsjd
 */
public class Crowbar extends JFrame
{
	//private JPanel p;
	private static final long								serialVersionUID					= 1;

	private List<ServerType>								_servers;
	private static Logger									softwareLogger						= null;
	private CrowbarSplash									_splashScreen;
	private Hashtable<JMenuItem, JToolBar>					_barHash
		= new Hashtable<JMenuItem, JToolBar>();
	private Hashtable<Object, ItemType>						_itemHash							= new Hashtable<Object, ItemType>();
	private CrowbarUser										_user;
	private final JMenuBar									_menuBar1							= new JMenuBar();
	private final JMenuBar									_menuBar2							= new JMenuBar();
	private final JMenuBar									_menuBar							= new JMenuBar();
	private final JPanel									_pnlToolbars						= new JPanel();
	private final JToolBar									_barServers							= new JToolBar();
	private final JToolBar									_barServers1						= new JToolBar();
	private final JButton									_server1Button						= new JButton();
	private final JButton									_server1Button1						= new JButton();
	private final JButton									_server1Button2						= new JButton();
	private final JDesktopPane								_desktopPane						= new JDesktopPane();
	private final JMenu										_mnFile								= new JMenu();
	private final JMenuItem									_mniExit							= new JMenuItem();
	private final JMenu										_mnEdit								= new JMenu();
	private final JMenuItem									_mniCut								= new JMenuItem();
	private final JMenuItem									_mniCopy							= new JMenuItem();
	private final JMenuItem									_mniPaste							= new JMenuItem();
	private Hashtable<CrowbarNetworkStatusChecker, Thread>	_checkerHash
		= new Hashtable<CrowbarNetworkStatusChecker, Thread>();
	private final JSplitPane								_pnlMain							= new JSplitPane();
	private final JTextPane									_txtHelpView						= new JTextPane();
	private int												_serverCount						= 0;
	private final JScrollPane								_scrollPane							= new JScrollPane();
	private final JPanel									_panel								= new JPanel();
	private final JButton									_btnHelpFrame						= new JButton();
	private final JButton									_xButton							= new JButton();
	private final Component									_component							= Box
																										.createHorizontalGlue();
	private final JPopupMenu								_mnServerPopup						= new JPopupMenu();
	private final JMenuItem									_mniShutdown						= new JMenuItem();
	private final JMenuItem									_mniReboot							= new JMenuItem();
	private int												_childTop							= -1;
	private int												_childLeft							= -1;
	private int												_childWindows						= 0;
	private int												_serverChecking						= 1;
	private CrowbarController								_controller;

	private boolean	_profileMismatchDisplaying													= false;

	/**
	 * @param args
	 */

	public Crowbar(CrowbarSplash splash, Hashtable<CrowbarNetworkStatusChecker, Thread> checkerHash)
	{
		super();
		_checkerHash = checkerHash;
		_splashScreen = splash;
		String devTitle = "";
		try
		{
			jbInit();
			softwareLogger = Logger.getLogger("global");
		}
		catch (Throwable e)
		{
			e.printStackTrace();
		}
		try
		{
			_controller = CrowbarMain.getController();
			_servers = _controller.getAllServers();
			// _menuBar2.add(_mnView);
			_pnlMain.setRightComponent(null);

			_splashScreen.renderSplashText("Loading server bar ...");
			loadServers();

			if (System.getenv("CROWBAR_DEV_MODE") == null)
			{
				softwareLogger.info("Syncing up users and environment . . .");
				_splashScreen.renderSplashText("Syncing up users and environment ...");
				_controller.updateLocalRoles();
				_controller.updateLocalUsers();
				_controller = CrowbarMain.createController();
			}
			else
			{
				devTitle = "DEVELOPMENT";
			}
			_user = _controller.getUser();

			// LDAP property will be set if the user has already been created
			String prop = CrowbarUser.getUserProperty(_user.getUser(), "LDAP");
			if (_user.getRole().getName() == null || (prop != null && prop.equalsIgnoreCase("1")))
			{
				// look the user up on the LDAP server
				// insert them into the local users.xml
				// if they are there and set their
				// role appropriately
				_splashScreen.renderSplashText("Querying LDAP for user ...");
				CrowbarLDAP ldap = new CrowbarLDAP(_controller);

				Role role = ldap.query(_user.getUsername());
				if (role != null)
				{
					_user.setRole(role);
					// set the LDAP property so we can identify them later if needed
					_user.setUserProperty("LDAP", "1");
					_user.getUser().setHidden(true);

					// if prop is not null then we just update their group to match
					// what came back from LDAP query
					if (prop == null)
					{
						// add them to the list and save them
						_controller.getUsers().add(_user.getUser());
					}

					_controller.saveUsersLocal();
				}
			}

			softwareLogger.info("Loading Toolbars and Menus . . .");
			_splashScreen.renderSplashText("Loading Toolbars and Menus . . .");

			loadToolbars();

			_menuBar2.add(Box.createHorizontalGlue());
			_menuBar1.add(Box.createHorizontalGlue());
			// ...create the rightmost menu...
			JLabel lblUser = new JLabel("Profile/User/Role: ");

			Color foreColor = new Color(50, 50, 255);
			lblUser.setForeground(foreColor);
			JLabel userName = new JLabel(_controller.getActiveProfile().getName() + " / "
					+ _user.getUsername() + " / " + _user.getRole().getName() + "  ");
			userName.setForeground(foreColor);
			userName.setFont(new Font("", Font.ITALIC, 12));
			_menuBar2.add(userName);

			softwareLogger.info("Configuring archive . . .");
			_splashScreen.renderSplashText("Configuring archive . . .");

			if (!_controller.mountNFSArchiveDrive())
			{
				softwareLogger.warning("Failed to mount or cannot access NFS archive.");
			}

			for (ServerType s : _controller.getAvailableServers())
			{
				if (s.getName().equalsIgnoreCase("nas"))
				{
					CrowbarCommand c = _controller.getCommand("CHECK_NAS_SNARE_CONFIG");
					c.addParameter("configfile", _controller.getValueOf("SnareConfigFile"));
					_controller.execute(c, s);
					break;
				}
			}

			_splashScreen.renderSplashText("Finishing setup . . .");

			String title = "CROWBAR - " + CrowbarMain.VERSION + "   " + devTitle;
			if (_controller.getValueOf("TechPubs").equalsIgnoreCase("1"))
			{
				title = "CROWBAR";
			}

			setTitle(title);
		}
		catch (Throwable e)
		{
			ByteArrayOutputStream output = new ByteArrayOutputStream();
			PrintStream p = new PrintStream(output);
			e.printStackTrace(p);
			softwareLogger.warning("Error during startup: \n" + e.getMessage() + "\n\nStack Trace:\n"
					+ output.toString());
		}
	}


	private JButton createButton(List<StepType> steps)
	{
		CrowbarDropButton button = new CrowbarDropButton(steps);
		button.setText("");
		button.setFocusable(false);
		button.setBorderPainted(false);
		button.setOpaque(false);
		if (steps.size() > 1)
		{
			button.setMaximumSize(new Dimension(40, 27));
			button.setPreferredSize(new Dimension(40, 27));
			button.setMinimumSize(new Dimension(40, 27));
		}
		else
		{
			button.setMaximumSize(new Dimension(25, 25));
			button.setPreferredSize(new Dimension(25, 25));
			button.setMinimumSize(new Dimension(25, 25));
		}
		button.setMargin(new Insets(0, 0, 0, 0));

		return button;
	}

	private Icon getIcon(String iconName)
	{
		Icon icon = null;
		if (iconName != null && !iconName.isEmpty())
		{
			icon = SwingResourceManager.getIcon(Crowbar.class, iconName);
			if (icon == null)
			{
				icon = new ImageIcon(iconName);
			}
		}
		return icon;
	}

	private boolean	_addSeparator	= false;

	private void processItem(Object menu, JToolBar pBar, ItemType item)
	{
		CrowbarController.entering(this.getClass().toString(), "processItem(" + item.getName() + ")");
		boolean bContinue = isAuthorized(item);

		if (bContinue)
		{
			// check to make sure the server is configured in servers.xml
			if (item.getId().startsWith("Shutdown -"))
			{
				String s = item.getServers().get(0);
				if (s != null && !s.isEmpty())
				{
					ServerType server = _controller.findServerByName(s);
					bContinue = (server.getIPAddress() != null);
				}
			}
		}

		if (bContinue)
		{
			if (item.getItems().size() > 0)
			{
				softwareLogger.finer("Item contains other items, processing them ...");
				JToolBar bar = new JToolBar();
				bar.setName("bar" + item.getName());
				bar.setMargin(new Insets(2, 0, -1, 0));
				bar.setBorderPainted(false);
				bar.setFloatable(false);
				JSeparator separator = new JSeparator();
				bar.add(separator);
				bar.add(new JToolBar.Separator());
				separator.setBorder(new BevelBorder(BevelBorder.LOWERED));
				separator.setMaximumSize(new Dimension(2, 25));
				separator.setPreferredSize(new Dimension(2, 2));

				if (menu instanceof JMenu)
				{
					if (_addSeparator)
					{
						((JMenu) menu).addSeparator();
						_addSeparator = false;
					}
				}
				JMenu m = new JMenu();
				m.setText(item.getName());
				m.setName("mn" + item.getName());
				if (item.getName().equalsIgnoreCase("File"))
				{
					m = _mnFile;
				}
				// if (item.getName().equalsIgnoreCase("View"))
				// {
				// m = _mnView;
				// }
				for (ItemType i : item.getItems())
				{
					processItem(m, bar, i);
				}
				if (menu instanceof JMenu)
				{
					if (m.getItemCount() > 0)
					{
						// only non-empty menus will be added
						((JMenu) menu).add(m);
					}
				}
				else if (menu instanceof JMenuBar)
				{
					if (m.getItemCount() > 0)
					{
						((JMenuBar) menu).add(m);
					}
					_addSeparator = false;
				}
				if (bar.getComponentCount() > 2)
				{
					bar.add(new JToolBar.Separator());
					_pnlToolbars.add(bar);
					JCheckBoxMenuItem barMenu = new JCheckBoxMenuItem();
					barMenu.setName("cmn" + item.getName());
					barMenu.setSelected(true);
					barMenu.setText(item.getName());
					barMenu.addActionListener(new ToolbarActionListner());
					_barHash.put(barMenu, bar);
					// _mnToolbars.add(barMenu);
				}
				bContinue = false;
			}
		}

		if (bContinue)
		{
			Icon icon = getIcon(item.getIcon());

			if (icon != null)
			{
				softwareLogger.finer("Item has an associated icon, creating toolbar button ...");
				List<StepType> steps = new ArrayList<StepType>();

				JButton button = createButton(steps);
				button.setName("btn" + item.getName());
				button.setIcon(icon);
				button.setToolTipText(item.getName());
				button.addActionListener(new GenericActionListner());
				_itemHash.put(button, item);
				pBar.add(button);
			}

			if (item.getName().isEmpty())
			{
				_addSeparator = true;
			}
			else
			{
				softwareLogger.finer("Creating menu item ...");
				if ((item.getItemClass() != null && !item.getItemClass().isEmpty() || item.getCommands() != null
						&& item.getCommands().size() > 0))
				{
					JMenuItem menuItem = new JMenuItem();
					menuItem.setName("mni" + item.getName());
					menuItem.setText(item.getName());
					menuItem.setIcon(icon);
					menuItem.addActionListener(new GenericActionListner());
					_itemHash.put(menuItem, item);
					if (menu instanceof JMenu)
					{
						if (_addSeparator)
						{
							((JMenu) menu).addSeparator();
							_addSeparator = false;
						}

						((JMenu) menu).add(menuItem);
					}
					else if (menu instanceof JMenuBar)
					{
						((JMenuBar) menu).add(menuItem);
						_addSeparator = false;
					}
				}
			}
			bContinue = false;
		}
		CrowbarController.exiting(this.getClass().toString(), "processItem()");
	}

	private boolean isAuthorized(ItemType item)
	{
		CrowbarController.entering(this.getClass().toString(), "isAuthorized(" + item.getName() + ")");
		boolean retVal = false;

		if (_user.isAllowed(item.getId()))
		{
			retVal = true;
		}
		CrowbarController.exiting(this.getClass().toString(), "isAuthorized(" + item.getName() + ") = "
				+ String.valueOf(retVal));
		return retVal;
	}

	private void loadToolbars()
	{
		CrowbarController.entering(this.getClass().toString(), "loadToolbars()");
		List<ItemType> items = _controller.getItems();

		JToolBar bar = new JToolBar();
		bar.setMargin(new Insets(2, 0, -1, 0));
		bar.setBorderPainted(false);
		bar.setFloatable(false);
		JSeparator separator = new JSeparator();
		bar.add(separator);
		bar.add(new JToolBar.Separator());
		separator.setBorder(new BevelBorder(BevelBorder.LOWERED));
		separator.setMaximumSize(new Dimension(2, 25));
		separator.setPreferredSize(new Dimension(2, 2));

		for (ItemType i : items)
		{
			if (i.getGroup() == 1)
			{
				processItem(_menuBar1, bar, i);
			}
			else
			{
				processItem(_menuBar2, bar, i);
			}
		}
		if (_menuBar1.getComponentCount() < 1)
		{
			_menuBar1.setVisible(false);
		}

		if (bar.getComponentCount() > 2)
		{
			bar.add(new JToolBar.Separator());
			_pnlToolbars.add(bar);
			JCheckBoxMenuItem barMenu = new JCheckBoxMenuItem();
			barMenu.setSelected(true);
			barMenu.setText("main");
			barMenu.addActionListener(new ToolbarActionListner());
			_barHash.put(barMenu, bar);
		}
		JToolBar lastBar = new JToolBar();
		lastBar.setMaximumSize(new Dimension(2000, 31));
		lastBar.setPreferredSize(new Dimension(0, 25));
		lastBar.setBorderPainted(false);
		lastBar.setFloatable(false);

		if (lastBar != null)
		{
			JPanel p = new JPanel();
			p.setPreferredSize(new Dimension(25, 25));
			p.setOpaque(false);
			lastBar.add(p);
		}
		lastBar.setName("lastbar");
		_pnlToolbars.add(lastBar);

		boolean monitorUPS = (_controller.getValueOf("DisableUPSMonitoring").equalsIgnoreCase("0"));

		if (monitorUPS)
		{
			JButton upsButton = new JButton();
			upsButton.setBorderPainted(false);

			upsButton.setToolTipText("UPS Status: WARNING: Missing");
			upsButton.setText("Missing");
			upsButton.setIcon(new ImageIcon("./rsc/battery-missing.png"));

			upsButton.setBackground(new Color(0, 0, 0, 0));
			upsButton.setOpaque(false);
			upsButton.setName("ups");
			upsButton.setMargin(new Insets(0, 0, 0, 0));
			upsButton.setBorderPainted(false);
			upsButton.setFocusable(false);
			upsButton.setHorizontalTextPosition(javax.swing.SwingConstants.LEADING);
			lastBar.add(upsButton);
		}

		CrowbarController.exiting(this.getClass().toString(), "loadToolbars()");
	}

	private JButton createServerButton(String serverName)
	{
		JButton button = new JButton();
		button.setMargin(new Insets(0, 0, 0, 0));
		button.setText(serverName);
		button.setBackground(Color.GRAY);
		button.addActionListener(new ServerButtonActionListener());

		if (!serverName.equalsIgnoreCase("printer"))
		{
			addPopup(button, _mnServerPopup);
		}

		return button;
	}

	private void loadServers()
	{
		CrowbarController.entering(this.getClass().toString(), "loadServers()");
		CrowbarController controller = CrowbarMain.getController();
		_servers = controller.getAllServers();

		controller.setLogCommands(false);
		_barServers.removeAll();
		for (ServerType server : _servers)
		{
			if (!server.isDevelopment())
			{
				_serverCount++;
				JButton button = createServerButton(server.getName());
				if (server.isAlive())
				{
					button.setBackground(Color.GREEN);
					chkProfile(server, button);
				}
				else
				{
					button.setBackground(Color.RED);
				}
				_barServers.add(button);
			}
		}

		// create a status checker for the monitor, adding button later
		boolean monitorUPS = (_controller.getValueOf("DisableUPSMonitoring")).equalsIgnoreCase("0");
		if (monitorUPS)
		{
			CrowbarController tmpController = controller.getNewController();
			tmpController.setLogCommands(false);
			ServerType server = tmpController.findServerByName("PowerMonitor");
			CrowbarNetworkStatusChecker checker = new UpsStatusChecker(tmpController, server);
			Thread t = new Thread(checker);
			t.start();
			_checkerHash.put(checker, t);
		}

		for (CrowbarNetworkStatusChecker c : _checkerHash.keySet())
		{
			c.addObserver(new ServerStatusObserver());
		}

		JButton button = new JButton();
		button.addActionListener(new ButtonActionListener());
		button.setMargin(new Insets(0, 0, 0, 0));
		button.setText("Refresh All");

		_barServers.add(button);
		_barServers.setFloatable(false);

		CrowbarController.exiting(this.getClass().toString(), "loadServers()");
	}

	private class ToolbarActionListner implements ActionListener
	{
		public void actionPerformed(final ActionEvent arg0)
		{
			JCheckBoxMenuItem item = (JCheckBoxMenuItem) arg0.getSource();
			if (_barHash.containsKey(item))
			{
				JToolBar bar = _barHash.get(item);
				bar.setVisible(item.isSelected());
			}
		}
	}

	private class GenericActionListner implements ActionListener
	{
		public void actionPerformed(final ActionEvent arg0)
		{
			genericActionPerformed(arg0);
		}
	}

	protected void genericActionPerformed(final ActionEvent arg0)
	{
		CrowbarController.entering(this.getClass().toString(), "genericActionPerformed()");
		if (_itemHash.containsKey(arg0.getSource()))
		{
			String step = "";
			if (arg0.getSource() instanceof CrowbarDropButton)
			{
				CrowbarDropButton b = (CrowbarDropButton) arg0.getSource();
				step = b.getSelectedStep();
				b.setSelectedStep("");
			}
			ItemType item = _itemHash.get(arg0.getSource());
			launchItem(item, step);
		}
		CrowbarController.exiting(this.getClass().toString(), "genericActionPerformed()");
	}

	public void launchItem(final ItemType item, final String step)
	{
		CrowbarController controller = CrowbarMain.createController();

		if (item == null)
		{
			softwareLogger.warning("ERROR: The item is null.");
			return;
		}
		CrowbarController.entering(this.getClass().getName(), "launchItem(" + item.getName() + ")");
		if ((_desktopPane.getAllFrames().length == 0))
		{
			controller.setCurrentItem(item);
			controller.setCurrentStep(step);
			int x = this.getLocationOnScreen().x;
			int y = this.getLocationOnScreen().y + this.getHeight();
			Dimension screenSize = Toolkit.getDefaultToolkit().getScreenSize();
			controller.allowRedirect();
			if (item.getItemClass() == null || item.getItemClass().isEmpty())
			{
				List<String> servers = new ArrayList<String>();
				servers.add(controller.getLocalHost().getName());
				if (item.getServers() != null && item.getServers().size() > 0)
				{
					servers = item.getServers();
				}
				String message = item.getConfirmationMessage();
				boolean userCanceled = false;
				if (message != null && !message.isEmpty())
				{
					int rtn = JOptionPane.showConfirmDialog(this, message, "Question", JOptionPane.YES_NO_OPTION);
					if (rtn != JOptionPane.YES_OPTION)
					{
						userCanceled = true;
					}
				}

				servers = _controller.moveLocalHostLast(servers);

				for (String sServer : servers)
				{
					ServerType server = controller.findServerByName(sServer);
					if (userCanceled)
					{
						continue;
					}
					if (server.isAlive())
					{
						List<CommandType> commands = item.getCommands();
						if (commands.size() > 0)
						{
							String tmpFile = "";
							try
							{
								boolean rtn = true;
								File tFile = File.createTempFile("Validation", "");
								tmpFile = tFile.getAbsolutePath();
								tFile.delete();
								for (CommandType command : commands)
								{
									CrowbarCommand c = new CrowbarCommand(command);

									List<String> commandParamLines = item.getCommandParameter();
									for (String commandParamLine : commandParamLines)
									{
										String parts[] = commandParamLine.split("\\|");

										if (parts[1].startsWith("~") && parts[1].endsWith("~"))
										{
											String varName = parts[1].replace("~", "");

											parts[1] = _controller.getValueOf(varName);
										}

										c.addParameter(parts[0], parts[1]);
									}

									// encrypted parameters
									EncryptUtil eu = new EncryptUtil();
									commandParamLines = item.getEncryptedCommandParameter();
									for (String commandParamLine : commandParamLines)
									{
										String parts[] = commandParamLine.split("\\|");

										if (parts[1].startsWith("~") && parts[1].endsWith("~"))
										{
											String varName = parts[1].replace("~", "");
											parts[1] = _controller.getValueOf(varName);
										}

										//System.out.println("decrypted=" + eu.decryptString(parts[1]));
										c.addParameter(parts[0], eu.decryptString(parts[1]));
										c.setMask(eu.decryptString(parts[1]));
									}

									String rootPath = controller.getValueOf("RootHelpPath");
									rootPath = new File(rootPath).getAbsolutePath();
									c.addParameter("file", tmpFile);
									c.addParameter("helppath", rootPath);
									c.addParameter("host", controller.getLocalHost().getIPAddress());
									c.addParameter("username", controller.getUser().getUsername());
									if (screenSize.height - y < 500)
									{
										c.addParameter("geometry", "+" + String.valueOf(x) + "+" + String.valueOf(100));
									}
									else
									{
										c.addParameter("geometry", "+" + String.valueOf(x) + "+" + String.valueOf(y));
									}

									// find the CD drive bay (if any)
									BayType cdBay = null;
									for (BayType bay : server.getBays())
									{
										if (bay.getDescription().equalsIgnoreCase("CD Drive"))
										{
											cdBay = bay;
											break;
										}
									}

									if (cdBay != null)
									{
										c.addParameter("cd_devicepath", cdBay.getDevicePath());
									}
									rtn = controller.execute(c, server);
									if (!c.getError().isEmpty())
									{
										softwareLogger.warning("Output:\n" + c.getOutput() + "\nError:\n"
												+ c.getError());
									}
									if (!rtn)
									{
										break;
									}
								}
								tFile.delete();
							}
							catch (Exception ex)
							{
								ex.printStackTrace();
								softwareLogger.warning("Failed to create temporary file.");
							}
						}
					}
					else
					{
						if (!item.isIgnoreDeadServers())
						{
							JOptionPane.showMessageDialog(this, "The server [" + server.getName()
									+ "] does not appear to be available.");
						}
					}
				}
			}
			else
			{
				Constructor< ? > c = getConstructor(item.getItemClass());
				if (c != null)
				{
					try
					{
						Object o = c.newInstance(controller);
						if (o instanceof JPanel)
						{
							JInternalFrame f = new JInternalFrame();
							f.getContentPane().add((JPanel) o);
							f.setResizable(true);
							f.setClosable(true);
							f.setMaximizable(true);
							f.setIconifiable(true);
							_desktopPane.add(f);
							f.setVisible(true);
							cascade(_desktopPane.getVisibleRect(), 24);
						}
						else if (o instanceof JInternalFrame)
						{
							JInternalFrame f;
							f = (JInternalFrame) o;
							_desktopPane.add(f);
							f.setVisible(true);
							cascade(_desktopPane.getVisibleRect(), 24);
						}
						else
						{
							_childTop = this.getLocation().y;
							if (this.getHeight() < 200)
							{
								_childTop += this.getHeight();
							}
							else
							{
								_childTop += 70;
							}
							_childLeft = this.getLocation().x;

							int left = _childLeft + (_childWindows * 20);
							int top = _childTop + (_childWindows * 20);
							JFrame f = (JFrame) o;
							f.setDefaultCloseOperation(DISPOSE_ON_CLOSE);
							_childWindows++;
							f.addWindowListener(new ChildWindowListener());

							if (screenSize.height - top < f.getSize().height)
							{
								top = 100 + (_childWindows * 20);
							}

							f.setLocation(left, top);
							f.setVisible(true);
							f.toFront();
						}
					}
					catch (Exception ex)
					{
						JOptionPane.showMessageDialog(this, ex.getMessage());
					}
				}
			}
		}
		else
		{
			softwareLogger.warning(" You already have a window open please close the current window and try again.");
		}
		CrowbarController.exiting(this.getClass().getName(), "launchItem");
	}

	private void cascade(final Rectangle dBounds, final int separation)
	{
		JInternalFrame frame = _desktopPane.getSelectedFrame();
		int margin = (_desktopPane.getAllFrames().length - 1) * separation;
		int x = dBounds.x + margin;
		int y = dBounds.y + margin;
		int width = (int) Math.min(dBounds.width - margin, frame.getPreferredSize().getWidth());
		int height = (int) Math.min(dBounds.height - margin, frame.getPreferredSize().getHeight());

		frame.setBounds(x, y, width, height);

	}

	private Constructor< ? > getConstructor(final String className)
	{
		Constructor< ? > co;

		try
		{
			Class< ? > cl = Class.forName(className);

			co = cl.getConstructor(new Class[]
			{CrowbarController.class});
		}
		catch (Exception ex)
		{
			co = null;
		}

		return co;
	}

	private void jbInit() throws Exception
	{
		setSize(new Dimension(700, 110));
		addWindowListener(new ThisWindowListener());
		setIconImage(SwingResourceManager.getImage(Crowbar.class, "/rsc/crowbarlogosmall.png"));
		setDefaultCloseOperation(WindowConstants.DO_NOTHING_ON_CLOSE);
		setTitle("Crowbar");
		setJMenuBar(_menuBar);
		_menuBar.setLayout(new BoxLayout(_menuBar, BoxLayout.Y_AXIS));
		_menuBar.add(_menuBar1);
		_menuBar.add(_menuBar2);
		_menuBar2.add(_mnFile);
		_mnFile.setText("File");
		_mnFile.add(_mniExit);
		_mniExit.addActionListener(new MniExitActionListener());
		_mniExit.setText("Exit");
		_mnEdit.addMenuListener(new MnEditMenuListener());
		_mnEdit.setText("Edit");
		_mnEdit.add(_mniCut);
		_mniCut.addActionListener(new DefaultEditorKit.CutAction());
		_mniCut.setText("Cut");
		_mnEdit.add(_mniCopy);
		_mniCut.addActionListener(new DefaultEditorKit.CopyAction());
		_mniCopy.setText("Copy");
		_mnEdit.add(_mniPaste);
		_mniCut.addActionListener(new DefaultEditorKit.PasteAction());
		_mniPaste.setText("Paste");
		// _mnView.setText("View");
		// _mnView.add(_mnToolbars);
		// _mnToolbars.setText("Toolbars");
		getContentPane().add(_pnlToolbars, BorderLayout.NORTH);
		_pnlToolbars.setBorder(new EmptyBorder(0, 0, 0, 0));
		_pnlToolbars.setLayout(new BoxLayout(_pnlToolbars, BoxLayout.X_AXIS));
		_pnlToolbars.setPreferredSize(new Dimension(0, 25));

		getContentPane().add(_barServers, BorderLayout.CENTER);

		_barServers.setLayout(new FlowLayout());
		_barServers.add(_server1Button);
		_server1Button.setBackground(Color.GREEN);
		_server1Button.setMargin(new Insets(0, 0, 0, 0));
		_server1Button.setText("Server1");

		_barServers.addSeparator();
		_barServers.add(_server1Button1);
		_server1Button1.setBackground(new Color(255, 0, 0));
		_server1Button1.setMargin(new Insets(0, 0, 0, 0));
		_server1Button1.setText("Server2");

		_barServers.addSeparator();
		_barServers.add(_server1Button2);
		_server1Button2.setBackground(new Color(0, 255, 0));
		_server1Button2.setMargin(new Insets(0, 0, 0, 0));
		_server1Button2.setText("Server3");

		_pnlMain.setDividerSize(3);

		_desktopPane.setBackground(Color.GRAY);
		_desktopPane.setPreferredSize(new Dimension(550, 500));
		_pnlMain.setLeftComponent(_desktopPane);
		_panel.setLayout(new BoxLayout(_panel, BoxLayout.X_AXIS));
		_panel.setMinimumSize(new Dimension(22, 22));
		_panel.setMaximumSize(new Dimension(7000, 22));
		_panel.setPreferredSize(new Dimension(22, 22));
		_panel.add(_component);
		_panel.add(_btnHelpFrame);
		_btnHelpFrame.setFocusable(false);
		_btnHelpFrame.setIconTextGap(0);
		_btnHelpFrame.setToolTipText("Show in external window");
		_btnHelpFrame.setMinimumSize(new Dimension(22, 22));
		_btnHelpFrame.addMouseListener(new XButtonMouseListener());
		_btnHelpFrame.setBorderPainted(false);
		_btnHelpFrame.setBackground(Color.BLUE);
		_btnHelpFrame.setOpaque(false);
		_btnHelpFrame.addActionListener(new BtnHelpFrameActionListener());
		_btnHelpFrame.setIcon(SwingResourceManager.getIcon(Crowbar.class, "/rsc/helpContents.png"));
		_btnHelpFrame.setMargin(new Insets(0, 0, 0, 0));
		_btnHelpFrame.setMaximumSize(new Dimension(22, 22));
		_btnHelpFrame.setPreferredSize(new Dimension(22, 22));

		_panel.add(_xButton);
		_xButton.setFocusable(false);
		_xButton.setPressedIcon(SwingResourceManager.getIcon(Crowbar.class, "/rsc/xSmallPressed.png"));
		_xButton.setIcon(SwingResourceManager.getIcon(Crowbar.class, "/rsc/xSmallNormal.png"));
		_xButton.setToolTipText("Close");
		_xButton.setMinimumSize(new Dimension(22, 22));
		_xButton.addMouseListener(new XButtonMouseListener());
		_xButton.addActionListener(new XButtonActionListener());
		_xButton.setBackground(Color.BLUE);
		_xButton.setBorderPainted(false);
		_xButton.setOpaque(false);
		_xButton.setComponentOrientation(ComponentOrientation.RIGHT_TO_LEFT);
		_xButton.setForeground(new Color(250, 128, 114));
		_xButton.setFont(new Font("Trebuchet MS", Font.BOLD, 14));
		_xButton.setMargin(new Insets(0, 0, 0, 0));
		_xButton.setMaximumSize(new Dimension(22, 22));
		_xButton.setPreferredSize(new Dimension(22, 22));

		_scrollPane.setViewportView(_txtHelpView);
		_txtHelpView.setContentType("text/html");
		_menuBar1.setName("menuBar1");
		_menuBar2.setName("menuBar2");
		_menuBar.setName("menuBar");

		_pnlToolbars.setName("pnlToolbars");
		_barServers.setName("barServers");
		_barServers1.setName("barServers1");
		_server1Button.setName("server1Button");
		addPopup(_server1Button, _mnServerPopup);

		_mnServerPopup.add(_mniShutdown);
		_mniShutdown.addActionListener(new MniShutdownActionListener());
		_mniShutdown.setText("Shutdown");
		_mnServerPopup.add(_mniReboot);
		_mniReboot.addActionListener(new MniRebootActionListener());
		_mniReboot.setText("Reboot");
		_server1Button1.setName("server1Button1");
		_server1Button2.setName("server1Button2");

		_desktopPane.setName("desktopPane");
		_mnFile.setName("mnFile");
		_mniExit.setName("mniExit");
		_mnEdit.setName("mnEdit");
		_mniCut.setName("mniCut");
		_mniCopy.setName("mniCopy");
		_mniPaste.setName("mniPaste");
		// _mnView.setName("mnView");
		// _mnToolbars.setName("mnToolbars");
		_pnlMain.setName("pnlMain");
		_txtHelpView.setName("txtHelpView");
	}

	private class MniExitActionListener implements ActionListener
	{
		public void actionPerformed(final ActionEvent arg0)
		{
			mniExitActionPerformed(arg0);
		}
	}

	private class ButtonActionListener implements ActionListener
	{
		public void actionPerformed(final ActionEvent arg0)
		{
			buttonActionPerformed(arg0);
		}
	}

	private class XButtonActionListener implements ActionListener
	{
		public void actionPerformed(final ActionEvent arg0)
		{
			xButtonActionPerformed(arg0);
		}
	}

	private class BtnHelpFrameActionListener implements ActionListener
	{
		public void actionPerformed(final ActionEvent arg0)
		{
			btnHelpFrameActionPerformed(arg0);
		}
	}

	private class XButtonMouseListener extends MouseAdapter
	{
		public void mouseEntered(final MouseEvent arg0)
		{
			xButtonMouseEntered(arg0);
		}

		public void mouseExited(final MouseEvent arg0)
		{
			xButtonMouseExited(arg0);
		}
	}

	private class MnEditMenuListener implements MenuListener
	{
		public void menuCanceled(final MenuEvent arg0)
		{
		}

		public void menuDeselected(final MenuEvent arg0)
		{
		}

		public void menuSelected(final MenuEvent arg0)
		{
			mnEditMenuSelected(arg0);
		}
	}

	private class MniShutdownActionListener implements ActionListener
	{
		public void actionPerformed(ActionEvent e)
		{
			mniShutdownActionPerformed(e);
		}
	}

	private class MniRebootActionListener implements ActionListener
	{
		public void actionPerformed(ActionEvent e)
		{
			mniRebootActionPerformed(e);
		}
	}

	private class ThisWindowListener extends WindowAdapter
	{
		public void windowClosed(WindowEvent e)
		{
			thisWindowClosed(e);
		}

		public void windowClosing(WindowEvent e)
		{
			thisWindowClosing(e);
		}
	}

	private class ChildWindowListener extends WindowAdapter
	{
		public void windowClosed(WindowEvent e)
		{
			childWindowClosed(e);
		}
	}

	private class ServerButtonActionListener implements ActionListener
	{
		public void actionPerformed(ActionEvent e)
		{
			serverButtonActionPerformed(e);
		}
	}

	protected void mniExitActionPerformed(final ActionEvent arg0)
	{
		shutdown();
	}

	private void shutdown()
	{
		int answer = JOptionPane.YES_OPTION;

		if (_childWindows > 0)
		{
			answer = JOptionPane
					.showConfirmDialog(this,
							"There are windows open that are associated with this one.\nDo you really want to close ALL windows?");
		}
		if (answer == JOptionPane.YES_OPTION)
		{
			for (CrowbarNetworkStatusChecker s : _checkerHash.keySet())
			{
				s.setShutdown();
				if (s.isSleeping())
				{
					_checkerHash.get(s).interrupt();
				}
			}

			this.dispose();
			System.exit(0);
		}

	}

	class ServerStatusObserver implements Observer
	{
		public void update(final Observable arg0, final Object arg1)
		{
			if (SwingUtilities.isEventDispatchThread())
			{
				// We are on the correct thread so do work
				if (arg1 instanceof ServerType)
				{
					ServerType server = (ServerType) arg1;
					String serverName = server.getName();
					if (_barServers != null)
					{
						for (Component c : _barServers.getComponents())
						{
							if (c instanceof JButton)
							{
								JButton b = (JButton) c;
								if (serverName.equalsIgnoreCase(b.getText()))
								{
									if (server.isAlive())
									{
										b.setBackground(Color.GREEN);
										chkProfile(server, b);
									}
									else
									{
										if (!_splashScreen.isVisible()
												&& (b.getBackground().equals(Color.GREEN) || b.getBackground().equals(Color.YELLOW)))
										{
											b.setBackground(Color.RED);
											JOptionPane.showMessageDialog(b, server.getName()
													+ " is no longer available!");
										}
										else
										{
											b.setBackground(Color.RED);
										}
									}
									if (_serverChecking < _serverCount)
									{
										_serverChecking++;
									}
									else
									{
										_serverChecking = 1;
										break;
									}
								}
							}
						}
					}
				}
				else if (arg1 instanceof String)
				{
					// This must be the UPS checker

					if (_pnlToolbars != null)
					{
						for (Component c : _pnlToolbars.getComponents())
						{
							if (c instanceof JToolBar)
							{
								JToolBar tb = (JToolBar) c;
								if (tb.getName() != null && tb.getName().equalsIgnoreCase("lastbar"))
								{
									for (Component c2 : tb.getComponents())
									{
										if (c2.getName() != null && c2.getName().equalsIgnoreCase("ups"))
										{
											String statusData = (String) arg1;
											JButton b = (JButton) c2;
											boolean isLowBattery = false;
											// low battery file used to control display of low battery dialog message
											File lowBatteryFile = new File("/tmp/lowbat");

											if (statusData.contains("-") && statusData.split("-").length == 2)
											{
												String data[] = statusData.split("-");
												String percentage = data[1] + "%";
												b.setText(percentage);

												if (data[0].equalsIgnoreCase("OL") || data[1].equalsIgnoreCase("100"))
												{
													b.setToolTipText("UPS Status: Charged");

													b.setIcon(new ImageIcon("./rsc/battery-full-charging.png"));
												}
												else if (data[0].equalsIgnoreCase("CHRG"))
												{
													b.setToolTipText("UPS Status: Charging");
													int percent = Integer.parseInt(data[1]);
													if (percent >= 90)
													{
														b.setIcon(new ImageIcon("./rsc/battery-full-charging.png"));
													}
													if (percent < 90)
													{
														b.setIcon(new ImageIcon("./rsc/battery-high-charging.png"));
													}
													if (percent < 80)
													{
														b.setIcon(new ImageIcon("./rsc/battery-medium-charging.png"));
													}
													if (percent < 70)
													{
														b.setIcon(new ImageIcon("./rsc/battery-caution-charging.png"));
													}
													if (percent < 50)
													{
														b.setIcon(new ImageIcon("./rsc/battery-low-charging.png"));
													}
												}
												else if (data[0].equalsIgnoreCase("DISCHRG"))
												{
													b.setToolTipText("UPS Status: WARNING: On Battery! ");

													int percent = Integer.parseInt(data[1]);
													if (percent >= 90)
													{
														b.setIcon(new ImageIcon("./rsc/battery-full.png"));
													}
													if (percent < 80)
													{
														b.setIcon(new ImageIcon("./rsc/battery-medium.png"));
													}
													b.setText("On Battery! " + percentage);
												}
												else if (data[0].equalsIgnoreCase("LB"))
												{
													isLowBattery = true;
													if (!lowBatteryFile.exists())
													{
														// create a temporary file to indicate the message has been shown
														try
														{
															lowBatteryFile.createNewFile();
														}
														catch (IOException e)
														{
															e.printStackTrace();
														}

														JOptionPane.showMessageDialog(b, "Low UPS Battery! "
																+ " Log out now. System will automatically shutdown.");
													}

													b.setToolTipText("UPS Status: WARNING: Low Battery!");
													b.setIcon(new ImageIcon("./rsc/battery-low.png"));
													b.setText("Low Battery! " + percentage);
												}
												else if (data[0].equalsIgnoreCase("STATE_NO_HID")
														|| data[0].equalsIgnoreCase("STATE_NO_COMM")
														|| data[0].equalsIgnoreCase("STATE_UNKNOWN"))
												{
													b.setToolTipText("UPS Status: WARNING: Missing");
													b.setText("Missing");
													b.setIcon(new ImageIcon("./rsc/battery-missing.png"));
												}

												if (!isLowBattery)
												{
													// clear the low battery warning
													try

													{
														lowBatteryFile.delete();
													}
													catch (RuntimeException e)
													{
														e.printStackTrace();
													}
												}
											}
											else
											{
												b.setToolTipText("UPS Status: WARNING: Missing");
												b.setText("Missing");
												b.setIcon(new ImageIcon("./rsc/battery-missing.png"));
											}
										}
									}
								}
							}
						}
					}
				}
			}
			else
			{
				Runnable callUpdate = new Runnable()
				{
					public void run()
					{
						update(arg0, arg1);
					}
				};
				SwingUtilities.invokeLater(callUpdate);
			}
		}

	}

	protected void buttonActionPerformed(final ActionEvent arg0)
	{
		for (Component c : _barServers.getComponents())
		{
			if (c instanceof JButton)
			{
				JButton b = (JButton) c;
				if (b != arg0.getSource())
				{
					b.setBackground(Color.GRAY);
				}
			}
		}
		for (CrowbarNetworkStatusChecker s : _checkerHash.keySet())
		{
			if (s.isSleeping())
			{
				_checkerHash.get(s).interrupt();
			}
			else
			{
				s.setFirstRun();
			}
		}
	}

	protected void mniContentsActionPerformed(final ActionEvent arg0)
	{
		launchHelpContents();
	}

	protected void xButtonActionPerformed(final ActionEvent arg0)
	{
		_xButton.setBackground(Color.BLUE);
		_xButton.setOpaque(false);
		_xButton.setBorderPainted(false);
		_pnlMain.setRightComponent(null);
	}

	protected void launchHelpContents()
	{
		if (_helpFrame == null)
		{
			_helpFrame = new JFrame();
			_helpFrame.getContentPane().setLayout(new BoxLayout(_helpFrame.getContentPane(), BoxLayout.X_AXIS));
			_helpFrame.setIconImage(SwingResourceManager.getImage(Crowbar.class, "/rsc/helpContents.PNG"));
			JScrollPane scroll = new JScrollPane();
			_helpFrame.getContentPane().add(scroll);
			JTextPane txtPane = new JTextPane();
			scroll.setViewportView(txtPane);
			txtPane.setContentType("text/html");
			txtPane.setEditable(false);
			try
			{
				txtPane.setPage("file:///dnloads/snoop.htm");
			}
			catch (Exception ex)
			{
				JOptionPane.showMessageDialog(this, "Failed to set help page.");
			}
			_helpFrame.setSize(400, 500);
			_helpFrame.setTitle("Help");
			_helpFrame.setResizable(true);
			_helpFrame.setLocationRelativeTo(this);
			_helpFrame.setVisible(true);
		}
		else
		{
			_helpFrame.setVisible(true);
		}
	}

	protected void btnHelpFrameActionPerformed(final ActionEvent arg0)
	{
		launchHelpContents();
		_btnHelpFrame.setBackground(Color.BLUE);
		_btnHelpFrame.setOpaque(false);
		_btnHelpFrame.setBorderPainted(false);
		_pnlMain.setRightComponent(null);
	}

	private JFrame	_helpFrame;

	protected void xButtonMouseEntered(final MouseEvent arg0)
	{
		JButton b = (JButton) arg0.getSource();
		b.setBorderPainted(true);
		b.setBackground(null);
		b.setOpaque(true);
	}

	protected void xButtonMouseExited(final MouseEvent arg0)
	{
		JButton b = (JButton) arg0.getSource();
		b.setBorderPainted(false);
		b.setBackground(Color.BLUE);
		b.setOpaque(false);
	}

	protected void mnEditMenuSelected(final MenuEvent arg0)
	{
		Component compFocusOwner = KeyboardFocusManager.getCurrentKeyboardFocusManager().getFocusOwner();
		Clipboard clipboard = this.getToolkit().getSystemClipboard();

		if (compFocusOwner instanceof JTextComponent)
		{
			_mniCut.setEnabled(true);
			_mniCopy.setEnabled(true);
			_mniPaste.setEnabled(clipboard.isDataFlavorAvailable(DataFlavor.stringFlavor));
			JTextComponent text = (JTextComponent) compFocusOwner;
			// get command table
			ActionMap actionMap = text.getActionMap();
			// Find specific commands
			Action cutAction = actionMap.get(DefaultEditorKit.cutAction);
			Action copyAction = actionMap.get(DefaultEditorKit.copyAction);
			Action pasteAction = actionMap.get(DefaultEditorKit.pasteAction);

			for (ActionListener a : _mniPaste.getActionListeners())
			{
				_mniPaste.removeActionListener(a);
			}
			for (ActionListener a : _mniCopy.getActionListeners())
			{
				_mniCopy.removeActionListener(a);
			}
			for (ActionListener a : _mniCut.getActionListeners())
			{
				_mniCut.removeActionListener(a);
			}
			_mniCut.addActionListener(cutAction);
			_mniCopy.addActionListener(copyAction);
			_mniPaste.addActionListener(pasteAction);

		}
		else
		{
			_mniCut.setEnabled(false);
			_mniCopy.setEnabled(false);
			_mniPaste.setEnabled(false);
		}
	}

	private static Component	popupComponent	= null;

	/**
	 * WindowBuilder generated method.<br>
	 * Please don't remove this method or its invocations.<br>
	 * It used by WindowBuilder to associate the {@link javax.swing.JPopupMenu} with parent.
	 */
	private static void addPopup(Component component, final JPopupMenu popup)
	{
		component.addMouseListener(new MouseAdapter()
		{
			public void mousePressed(MouseEvent e)
			{
				if (e.isPopupTrigger())
				{
					showMenu(e);
				}
			}

			public void mouseReleased(MouseEvent e)
			{
				if (e.isPopupTrigger())
				{
					showMenu(e);
				}
			}

			private void showMenu(MouseEvent e)
			{
				popupComponent = e.getComponent();
				popup.show(e.getComponent(), e.getX(), e.getY());
			}
		});
	}

	protected void mniShutdownActionPerformed(ActionEvent e)
	{
		if (popupComponent instanceof JButton)
		{
			String serverName = ((JButton) popupComponent).getText();
			int answer = JOptionPane.showConfirmDialog(this, "Are you sure you want to shutdown [" + serverName + "]?",
					"Question", JOptionPane.YES_NO_OPTION);
			if (answer == JOptionPane.YES_OPTION)
			{
				ServerType server = _controller.findServerByName(serverName);
				if (server.isAlive())
				{
					List<String> shutdownList = new ArrayList<String>();
					shutdownList.add(server.getName());
					_controller.doShutdown(shutdownList);
				}
			}
		}
	}

	protected void mniRebootActionPerformed(ActionEvent e)
	{
		if (popupComponent instanceof JButton)
		{
			String serverName = ((JButton) popupComponent).getText();
			int answer = JOptionPane.showConfirmDialog(this, "Are you sure you want to reboot [" + serverName + "]?",
					"Question", JOptionPane.YES_NO_OPTION);
			if (answer == JOptionPane.YES_OPTION)
			{
				ServerType server = _controller.findServerByName(serverName);
				if (server.isAlive())
				{
					List<String> rebootList = new ArrayList<String>();
					rebootList.add(server.getName());
					_controller.doRestart(rebootList);
				}
			}
		}
	}

	protected void childWindowClosed(WindowEvent e)
	{
		_childWindows--;
	}

	protected void thisWindowClosed(WindowEvent e)
	{
		for (CrowbarNetworkStatusChecker s : _checkerHash.keySet())
		{
			s.setShutdown();
			if (s.isSleeping())
			{
				_checkerHash.get(s).interrupt();
			}
		}
	}

	protected void thisWindowClosing(WindowEvent e)
	{
		shutdown();
	}

	protected void serverButtonActionPerformed(ActionEvent e)
	{
		Object c = e.getSource();
		if (c instanceof JButton)
		{
			JButton b = (JButton) c;
			b.setBackground(Color.GRAY);
		}
		for (CrowbarNetworkStatusChecker s : _checkerHash.keySet())
		{
			if (s.isSleeping())
			{
				_checkerHash.get(s).interrupt();
			}
			else
			{
				s.setFirstRun();
			}
		}
	}

	private void chkProfile(final ServerType server, final JButton b)
	{
		if (_controller.getValueOf("SkipMismatch").equalsIgnoreCase("true"))
		{
			return;
		}

		String hostProfile = new String();
		CrowbarCommand command;
		boolean retVal;
		String profileParts[];

		if (server.isSkipConfiguration() || !server.isAlive())
		{
			return;
		}

		command = _controller.getCommand("GetHostProfile");
		command.setSuppressWarnings(true);

		final int loopMax = 5;
		final int sleepTime = 15000;
		for (int i = 0; i < loopMax; i++)
		{
			_controller.execute(command, server);

			String hostProfileData = command.getOutput().trim();
			retVal = hostProfileData.startsWith("PF:");

			if (retVal)
			{
				// the script executed
				profileParts = hostProfileData.split(":");

				if (profileParts.length == 2)
				{
					hostProfile = profileParts[1];
				}

				if (hostProfile.equalsIgnoreCase(_controller.getActiveProfile().getId()))
				{
					// the host profile matches the active profile
					// OR the command did not successfully execute
					b.setToolTipText("");
					return;
				}
			}
			else
			{
				// do not know if the profile matches since command did not execute
				// set the profile bit so no warning occurs
				if (i == loopMax - 1)
				{
					softwareLogger.info("chkProfile() - giving up; failed to execute command on " + server.getName());
					b.setToolTipText("");
					return;
				}
				try
				{
					softwareLogger.info("chkProfile() - sleeping; failed to execute command on " + server.getName());
					Thread.sleep(sleepTime);
				}
				catch (InterruptedException e)
				{
					e.printStackTrace();
				}
			}
		}

		b.setToolTipText("Warning - Profile [" + hostProfile + "] does not match active profile.");
		Runnable guiUpdate = new Runnable()
		{
			public void run()
			{
				b.setBackground(Color.YELLOW);

				if (_profileMismatchDisplaying)
				{
					// don't show the notification again
					return;
				}

				Component parent = KeyboardFocusManager.getCurrentKeyboardFocusManager().getActiveWindow();

				ReentrantLock mutex = new ReentrantLock();
				if (CrowbarMain.getSplash() != null)
				{
					mutex = CrowbarMain.getSplash().getMutex();
				}

				try
				{
					// Adding mutex code to make sure the slash screen visibility is not modified
					// while the notice is displayed. Otherwise it's possible this thread would
					// change the visibility back to true after main() has already closed
					// the splash screen object.

					String errorMessage = "Configuration mismatch detected for one or more hosts. Hosts\n"
					+ " that do not match the current configuration will be highlighted yellow\n"
					+	" in the server status bar.";

					mutex.lock();

					if (CrowbarMain.getSplash() != null)
					{
						CrowbarMain.getSplash().setVisibility(false);
					}

					_profileMismatchDisplaying = true;
					JOptionPane.showMessageDialog(parent, errorMessage, "Configuration Error", JOptionPane.WARNING_MESSAGE);
					_profileMismatchDisplaying = false;

					if (CrowbarMain.getSplash() != null && !CrowbarMain.isStartupComplete())
					{
						CrowbarMain.getSplash().setVisibility(true);
					}
				}
				finally
				{
					mutex.unlock();
				}
			}
		};

		if (SwingUtilities.isEventDispatchThread())
		{
			guiUpdate.run();
		}
		else
		{
			SwingUtilities.invokeLater(guiUpdate);
		}
	}
}
