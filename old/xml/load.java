if(! _serverFile.isEmpty()) {
  loadServers();
}

public void loadServers()
{
  SAToolbarJAXB saJAXB = SAToolbarJAXB.getInstance();
  try
  {
    SAToolbarServerList list = satJAXB.parseServerFile(this._serverFile);
    this._servers = list.getServers();
  }
  catch (JAXBException e)
  {
    e.printStackTrace();
  }
}

